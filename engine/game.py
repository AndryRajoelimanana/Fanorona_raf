from board.Board import Board, MoveGenerator


class Game:
    def __init__(self):
        self.board = Board.initial_board()

    def move(self, from_, to_):
        if from_ == self.board:
            self.board = to_
            # print(self.board)
        else:
            raise "board not equal to from_"

    def get_board(self):
        return self.board

    def set_board(self, b):
        if b is None:
            raise 'Board cannot be None'
        # temp = b
        self.board = b

        # self.board.prev = temp

    def reset_board(self):
        b = Board.initial_board()
        self.set_board(b)

    @staticmethod
    def must_pass(brd: Board):
        if not brd.mid_capture():
            return False
        mg = MoveGenerator(brd)
        return mg.nextSet() == 0
