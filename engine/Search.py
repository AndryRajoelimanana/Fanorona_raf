import os
import sys
sys.path.append(os.path.realpath('..'))
from board.Board import Board
from board.Board import Boardmove
from engine.MoveGenerator import MoveGenerator

import time


def current_milli_time():
    return int(round(time.time() * 1000))


class Search:
    searchBound = 7200
    ASPIRATION_WINDOW = 50
    currentEval = 0
    time_max = 5000

    def __init__(self, board, ply=0):
        self.stop = False
        self.watcher = None
        self.firstMove = None
        self.board = board
        self.ply = ply
        self.move = None
        self.move_log = []
        time.sleep(0)

        if Board.mustPass(self.board):
            print('Forced pass')
            new_board_move = Boardmove(self.board, 0)
            self.set_board_move(new_board_move)
            self.done()
            return

        mg = MoveGenerator(self.board)
        if not (mg.hasMoreElements()):
            return

        new_board_move = Boardmove(self.board, mg.nextSet())
        self.set_board_move(new_board_move)
        if not (mg.hasMoreElements()):
            print("Forced move")
            self.done()
            return

        if Board.endgameDatabase is not None:
            self.set_board_move(self.board.principalVariation)
            self.done()
            return

        self.search()

    def get_stop(self):
        return self.stop

    def set_stop(self, s):
        self.stop = s

    def get_board_move(self):
        return self.move

    def set_board_move(self, m):
        self.move = m

    def make_board_move(self):
        move = self.get_board_move()
        if move is None:
            newmg = MoveGenerator(self.board)
            move = Boardmove(self.board, newmg.nextSet())
        self.move = move

    def abort(self):
        print("Position changed while searching, search aborted")
        Board.sequence_number += 1  # terminate currently running search

    def panic(self):
        Board.sequence_number += 1  # terminate currently running search
        print("Search timed out, making move without finishing search")
        self.make_board_move()

    def done(self):
        self.make_board_move()
        self.board.child = None
        self.board.principalVariation = None
        self.board.moveGenerator = None

    def search(self):
        depth = 1
        log_disabled = False
        previous_eval = 0
        self.move_log = []
        self.board.bestMove = -1
        Board.sequence_number = Board.sequence_number + 1
        sequence_number = Board.sequence_number
        while ((self.ply == 0) or (depth <= self.ply)) and (not (self.get_stop())):
            Board.nodeCount = 0
            Board.leafCount = 0
            if Board.collect_extra_statistics:
                Board.boardConsCount = 0
                Board.moveGenConsCount = 0
                Board.endgameEvalCount = 0
                Board.pvChangeCount = 0

            start_time = current_milli_time()

            alpha = Search.currentEval - int(Search.ASPIRATION_WINDOW / 2)
            beta = Search.currentEval + int(Search.ASPIRATION_WINDOW / 2)
            aspirations = 0
            while True:
                if sequence_number != Board.sequence_number:
                    self.abort()
                    return
                self.board.alpha_beta(depth * Board.ply, alpha, beta, sequence_number)
                Search.currentEval = self.board.evaluation
                aspirations += 1
                if (current_milli_time() - start_time) > Search.time_max:
                    self.done()
                    break
                if Search.currentEval >= beta:
                    beta = Board.maxsize
                elif Search.currentEval <= alpha:
                    alpha = -Board.maxsize
                else:
                    break
                time.sleep(0)

            if Search.winning(previous_eval) and (not Search.between(0, previous_eval, Search.currentEval)):
                Search.currentEval = previous_eval
            elif self.board.principalVariation is not None:
                self.set_board_move(Boardmove(self.board, self.board.bestMove))
            if (not log_disabled) or (Search.currentEval != previous_eval):
                previous_eval = Search.currentEval
            if Search.winning(Search.currentEval) and (not log_disabled):
                print("Winning line found, searching for better win")
                log_disabled = True
            depth += 1
            time.sleep(0)

        self.done()

    @staticmethod
    def winning(evals):
        return (evals < -Search.searchBound) or (evals > Search.searchBound)

    @staticmethod
    def between(a, b, c):
        if a <= b <= c:
            return True
        else:
            return False
