from flask import Flask, render_template, request, jsonify, session
from board.Board import Board, Boardmove, SetBoard
from Utils import utils
from engine.Search import Search
from flask_cors import CORS

app = Flask(__name__, template_folder="webapp/fanoronaraf/public/")
CORS(app)

app.secret_key = '\xb3j\x9e\xeeD&g\xa4\xcd\xdeH\xa4\x0fT\xc4+\xdf\x04H{_\xa0\xe0g'


@app.route('/')
def index():
    board_class = Board()
    board = utils.PiecesOnBoard(board_class.myPieces, board_class.opponentPieces)
    return render_template("/home/andry/PycharmProjects/Fanorona/webapp/fanoronaraf/public/index.html", board=board)


@app.route("/pass", methods=["GET", "POST"])
def pass_game():
    board = request.get_json('boardstate')
    my_pieces, opp_pieces = utils.board_to_bit(board)
    my_board = SetBoard(my_pieces, opp_pieces)
    search_obj = Search(my_board, ply=3)
    move_log = []
    b_search = search_obj.board
    while not b_search.human_to_move():
        new_search = Search(b_search, ply=3)
        move = new_search.board.best_move
        b_search = Boardmove(new_search.board, move)
        move_log.append(move)
    new_board = new_search.board.previousPosition
    board_pieces = utils.bit_to_pieces(new_board)
    return jsonify({'boardstate': board_pieces, 'move_log': move_log})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
