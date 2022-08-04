from flask import Flask, render_template, request, jsonify
from board.Board import Board
from engine.game import Game
from engine.Search import run_search
from Utils.utils import Player, board_to_bit, PiecesOnBoard
# from flask_cors import CORS

app = Flask(__name__, template_folder="static/react")
# CORS(app)

app.secret_key = '\xb3j\x9e\xeeD&g\xa4\xcd\xdeH\xa4\x0fT\xc4+\xdf\x04H{_\xa0\xe0g'


@app.route('/')
def index():
    board_class = Board.initial_board()
    board = PiecesOnBoard(board_class.myPieces, board_class.oppPieces)
    return render_template("index.html")
    #return jsonify(board.myPieces.value, board.oppPieces.value)


@app.route("/pass", methods=["GET", "POST"])
def pass_game():
    in_board = request.get_json()
    board = in_board['boardstate']
    print(board)
    was_capture = in_board['was_capture']
    depth = int(in_board['depth'])
    my_pieces, opp_pieces = board_to_bit(board)
    my = Player(my_pieces)
    opp = Player(opp_pieces | (int(was_capture) << 63) | (1 << 62))
    board = Board(my, opp)
    # print(board.myPieces.repr, board.oppPieces.repr)
    game = Game()
    game.set_board(board)
    run_search(game, depth)
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
            move_pos = (cur.best_move & cur.myPieces).to_pos(True)+1
            moves.append((move_pos, [0]))
            first_move = False
        move_pos = (cur.best_move & cur.open).to_pos(True)+1
        move_ = cur.best_move.all_one()
        moves.append((move_pos, move_))
        cur = cur.next
        if cur.best_move <= 0:
            break
    return jsonify({'move_log': moves})
    #
    #
    #
    #
    # in_board = request.get_json()
    # board = in_board['boardstate']
    # was_capture = in_board['was_capture']
    # depth = int(in_board['depth'])
    # my_pieces, opp_pieces = utils.board_to_bit(board)
    # my_pieces = utils.Player(my_pieces)
    # opp_pieces = utils.Player(opp_pieces | was_capture)
    # my_board = Board(my_pieces, opp_pieces)
    # print(my_board.myPieces, my_board.oppPieces)
    # move_log = []
    # new_search = Search(my_board, ply=depth)
    # while not b_search.human_to_move():
    #     new_search = Search(b_search, ply=depth)
    #     if new_search.board.forced:
    #         move = new_search.board.arbmove
    #     else:
    #         move = new_search.board.best_move
    #
    #     b_search = Boardmove(new_search.board, move)
    #     if move > 0:
    #         print(move)
    #         if len(move_log) == 0:
    #             selected = utils.findPiece(new_search.board.myPieces & move)[0]
    #             move_log.append(selected)
    #             movedict[str(selected)] = [0]
    #         selected = utils.findPiece(~(new_search.board.myPieces | new_search.board.oppPieces | (1 << (selected - 1))) & move)[0]
    #         move_log.append(selected)
    #         movedict[str(selected)] = utils.findPiece(new_search.board.oppPieces & move)
    # jj = jsonify({'move_log': move_log, 'movedict': movedict})
    #
    #

    # while not b_search.human_to_move():
    #     new_search = Search(b_search, ply=depth)
    #     if new_search.board.forced:
    #         move = new_search.board.arbmove
    #     else:
    #         move = new_search.board.best_move
    #
    #     b_search = Boardmove(new_search.board, move)
    #     if move > 0:
    #         print(move)
    #         if len(move_log) == 0:
    #             selected = utils.findPiece(new_search.board.myPieces & move)[0]
    #             move_log.append(selected)
    #             movedict[str(selected)] = [0]
    #         selected = utils.findPiece(~(new_search.board.myPieces | new_search.board.oppPieces | (1 << (selected - 1))) & move)[0]
    #         move_log.append(selected)
    #         movedict[str(selected)] = utils.findPiece(new_search.board.oppPieces & move)

    # return jsonify({'move_log': move_log, 'movedict': movedict})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
