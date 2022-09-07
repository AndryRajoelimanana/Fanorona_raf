from flask import Flask, render_template, request, jsonify, Response
from board.Board import Board
from engine.game import Game
from engine.Search import run_search, Search
from Utils.utils import Player, board_to_bit, PiecesOnBoard
import time
# from flask_sse import sse
import redislite
from flask_cors import CORS
import json

app = Flask(__name__, template_folder="static/react")
CORS(app)

redis = redislite.StrictRedis('/tmp/redis_db.db', decode_responses=True)

app.secret_key = '\xb3j\x9e\xeeD&g\xa4\xcd\xdeH\xa4\x0fT\xc4+\xdf\x04H{_\xa0\xe0g'


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/pass", methods=["GET", "POST"])
def pass_game():
    in_board = request.get_json()
    board = in_board['boardstate']
    depth = int(in_board['depth'])
    midcapture = int(in_board['midcapture'])
    maxtime = int(in_board['maxtime'])
    print(board, depth, midcapture, maxtime, 'ggggg')
    my_pieces, opp_pieces = board_to_bit(board)
    my = Player(my_pieces)
    opp = Player(opp_pieces | (1 << 62) | (midcapture << 63))
    board = Board(my, opp)
    game = Game()
    game.set_board(board)
    start = time.time()
    run_search(game, depth, maxtime)
    gg = game.board
    moves = []
    # find pointer head
    head = gg
    while head.prev:
        head = head.prev

    cur = head
    first_move = True
    while cur.next:
        if first_move:
            move_pos = (cur.best_move & cur.myPieces).to_pos(True) + 1
            moves.append((move_pos, [0]))
            first_move = False
        move_pos = (cur.best_move & cur.open).to_pos(True) + 1
        move_ = cur.best_move.all_one()
        moves.append((move_pos, move_))
        cur = cur.next
        if cur.best_move <= 0:
            break
    print('vita', moves)
    return json.dumps({'move_log': moves})


def event_stream():
    while True:
        move = redis.rpop('moves3')
        if not move:
            yield json.dumps({'move_log': [0]})
        f = json.dumps(move)
        print('moves3', move, f)
        # if len(f['move_log']) == 0:
        #     break
        yield f
    return 'done'


@app.route("/stream", methods=["GET"])
def stream():
    print(redis.lrange('moves', 0, -1))
    move = redis.rpop('moves')
    print(json.dumps(move))
    if move:
        # response = Response(move, mimetype="text/json")
        # response = Response(move, mimetype='text/event-stream')
        response = jsonify(move)
    else:
        response = Response(json.dumps({'move_log': [0]}),
                            mimetype='text/event-stream')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/pass1", methods=["GET", "POST"])
def pass_game1():
    in_board = request.get_json()
    board = in_board['boardstate']
    depth = int(in_board['depth'])
    midcapture = int(in_board['midcapture'])
    maxtime = int(in_board['maxtime'])
    print(board, depth, maxtime)
    my_pieces, opp_pieces = board_to_bit(board)
    my = Player(my_pieces)
    opp = Player(opp_pieces | (1 << 62) | (midcapture << 63))
    board = Board(my, opp)
    game = Game()
    game.set_board(board)
    step = 1
    redis.delete('moves')
    while not board.human_to_move():
        start = time.time()
        board = game.get_board()
        search = Search(game, board, ply=depth, time_max=maxtime)
        search.run()
        print(f'step: {step} took {time.time() - start}')
        step += 1
        board = game.get_board()
        if not board.prev:
            print('tato prevc')
            redis.lpush('moves', json.dumps({'move_log': [0]}))
            return {'move_log': [0]}
        if board.prev.best_move < 0:
            print('tato neg')
            redis.lpush('moves', json.dumps({'move_log': [0]}))
            return {'move_log': [0]}
        moves = board.prev.best_move.all_one()
        print({'move_log': moves})
        redis.lpush('moves', json.dumps({'move_log': moves}))
    redis.lpush('moves', json.dumps({'move_log': [0]}))
    return jsonify({"status": 204})


if __name__ == '__main__':
    app.run(debug=True)
