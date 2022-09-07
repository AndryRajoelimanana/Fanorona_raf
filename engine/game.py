from board.Board import Board, MoveGenerator
import weakref


class Observable(object):
    def __init__(self, board):
        self.board = board
        self.observers = weakref.WeakKeyDictionary()

    def set_board(self, board):
        if board is None:
            raise 'Board cannot be None'
        self.board = board
        self.notifyObservers(self.board)

    def get_board(self):
        return self.board

    def addObserver(self, o):
        self.observers[o] = 1

    def removeObserver(self, o):
        del self.observers[o]

    def notifyObservers(self, new):
        for o in self.observers:
            o.update_board(new)


class Game(Observable):
    def __init__(self):
        board = Board.initial_board()
        super(Game, self).__init__(board)

    def move(self, from_, to_):
        if from_ == self.board:
            self.set_board(to_)
        else:
            print(from_)
            print(self.board)
            raise "board not equal to from_"

    def reset_board(self):
        b = Board.initial_board()
        self.set_board(b)

    @staticmethod
    def must_pass(brd: Board):
        if not brd.mid_capture():
            return False
        mg = MoveGenerator(brd)
        return mg.nextSet() == 0
