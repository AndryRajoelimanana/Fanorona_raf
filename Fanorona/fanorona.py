from flask import Flask, render_template, request, jsonify, session
from board.Board import Board, Boardmove, SetBoard
from engine.MoveGenerator import MoveGenerator
from Utils import utils
from engine.Search import Search
from flask_cors import CORS

app = Flask(__name__, template_folder="static/react/")
CORS(app)



app.secret_key = '\xb3j\x9e\xeeD&g\xa4\xcd\xdeH\xa4\x0fT\xc4+\xdf\x04H{_\xa0\xe0g'


@app.route('/')
def index():
    board_class = Board()
    board = utils.PiecesOnBoard(board_class.myPieces, board_class.opponentPieces)
    return render_template("index.html", board=board)


@app.route("/pass", methods=["GET", "POST"])
def pass_game():
    in_board = request.get_json()
    board = in_board['boardstate']
    was_capture = in_board['was_capture']
    my_pieces, opp_pieces = utils.board_to_bit(board)
    my_board = SetBoard(my_pieces, opp_pieces)
    # my_board = Boardmove(my_board, 0)
    print(my_board.myPieces, my_board.opponentPieces)
    move_log = []
    movedict = dict()
    # search_obj = Search(my_board, ply=3)
    # move_log.append(search_obj.board.best_move)
    b_search = my_board
    while not b_search.human_to_move():
        new_search = Search(b_search, ply=3)
        if new_search.board.forced:
            print('tato')
            move = new_search.board.arbmove
        else:
            move = new_search.board.best_move

        b_search = Boardmove(new_search.board, move)
        if move > 0:
            print(move)
            if len(move_log) == 0:
                selected = utils.findPiece(new_search.board.myPieces & move)[0]
                move_log.append(selected)
                movedict[str(selected)] = [0]
            selected = utils.findPiece(~(new_search.board.myPieces | new_search.board.opponentPieces | (1 << (selected-1))) & move)[0]
            move_log.append(selected)
            movedict[str(selected)] = utils.findPiece(new_search.board.opponentPieces & move)

    print(move_log, movedict)
    return jsonify({'move_log': move_log, 'movedict': movedict})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
