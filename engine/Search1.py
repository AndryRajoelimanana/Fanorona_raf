import os
import sys

sys.path.append(os.path.realpath('..'))

from Utils.utils1 import *

from board.Board1 import Board
from board.Board1 import MoveGenerator

import time


def current_milli_time():
    return int(round(time.time() * 1000))


class Search:
    searchBound = 7200
    ASPIRATION_WINDOW = 50
    currentEval = 0
    time_max = 5000

    def __init__(self, game, boardin, ply=3):
        self.stop = False
        self.watcher = None
        self.firstMove = None
        self.board = boardin
        self.ply = ply
        self.move = None
        self.move_log = []
        self.game = game
        time.sleep(0)

        if Game.must_pass(self.board):
            print('Forced pass')
            new_board_move = Board.from_move(self.board, Piece(0))
            self.set_board_move(new_board_move)
            self.done()
            return

        mg = MoveGenerator(self.board)
        if not (mg.hasMoreElements()):
            return

        nextmove = mg.nextSet()
        new_board_move = Board.from_move(self.board, nextmove)
        self.set_board_move(new_board_move)
        if not (mg.hasMoreElements()):
            print("Forced move")
            # self.board.forced = True
            # self.board.arbmove = nextmove
            self.done()
            return

        if Board.endgameDatabase is not None:
            self.set_board_move(self.board.PVar)
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
        board = self.board
        if move is None:
            newmg = MoveGenerator(board)
            move = Board.from_move(board, newmg.nextSet())
        # if self.board == move:
        # self.board = move
        self.game.move(board, move)
        # self.move = move

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
        self.board.PVar = None
        self.board.moveGenerator = None

    def search(self):

        depth = 1
        log_disabled = False
        previous_eval = 0
        self.move_log = []
        self.board.best_move = Piece(-1)
        Board.sequence_number += 1
        sequence_number = Board.sequence_number
        while ((self.ply == 0) or (depth <= self.ply)) and (
                not (self.get_stop())):
            Board.nodeCount = Board.leafCount = 0
            if Board.collect_extra_statistics:
                Board.boardConsCount = Board.moveGenConsCount = 0
                Board.endgameEvalCount = Board.pvChangeCount = 0

            if Hash.collect_statistic_hash:
                Hash.hits = Hash.misses = Hash.shallow = Hash.badBound = 0

            start_time = current_milli_time()

            aspirations_window = int(Search.ASPIRATION_WINDOW / 2)
            alpha = Search.currentEval - aspirations_window
            beta = Search.currentEval + aspirations_window
            aspirations = 0
            while True:
                if sequence_number != Board.sequence_number:
                    self.abort()
                    return
                dpth = depth * Board.ply
                self.board.alpha_beta(dpth, alpha, beta, sequence_number)
                Search.currentEval = self.board.evaluation
                if debug:
                    print(f'New Search: {self.board.myPieces.repr} '
                          f'{self.board.oppPieces.repr} {depth}')
                aspirations += 1
                if debug:
                    print(f'Search eval: {Search.currentEval} {alpha} {beta}')
                if Search.currentEval >= beta:
                    beta = Board.maxsize
                elif Search.currentEval <= alpha:
                    alpha = -Board.maxsize
                else:
                    break
                # time.sleep(0.1)

            if Search.winning(previous_eval) and (
                    not Search.between(0, previous_eval, Search.currentEval)):
                Search.currentEval = previous_eval
            elif self.board.PVar is not None:
                new_board = Board.from_move(self.board, self.board.best_move)
                self.set_board_move(new_board)
            if (not log_disabled) or (Search.currentEval != previous_eval):
                previous_eval = Search.currentEval
                exec_time = current_milli_time() - start_time + 1
                hash_stat = ''
                if Hash.collect_statistic_hash:
                    total_hash = Hash.total_hash()
                    hits_rate = int((Hash.hits * 100) / total_hash)
                    max_rate = int(100 * (Hash.hits + Hash.shallow +
                                          Hash.badBound) / total_hash)
                    hash_stat = f', hash rate {hits_rate}%- {max_rate}%'
                print(f'{depth} ply: {Search.currentEval / 100},'
                      f' {Board.nodeCount} '
                      f'nodes, {Board.leafCount} leaves, '
                      f'{int(Board.nodeCount / exec_time)}k nps {hash_stat}')

            self.board.print_PVar()
            if Search.winning(Search.currentEval) and (not log_disabled):
                print("Winning line found, searching for better win")
                log_disabled = True
            depth += 1
            time.sleep(0.1)

        self.done()

    @staticmethod
    def winning(evals):
        return (evals < -Search.searchBound) or (evals > Search.searchBound)

    @staticmethod
    def between(a, b, c):
        """ ((a <= b <= c)  OR (c <= b <= a)) AND a != c"""
        return (a >= b) != (c >= b)


class Game:
    def __init__(self):
        self.board = Board.initial_board()

    def move(self, from_, to_):
        if from_ == self.board:
            self.board = to_
        else:
            print('nnnnnn')

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


def run_search(game, ply=3):
    while True:
        board = game.get_board()
        # print(board)
        if board.human_to_move():
            break
        print('\n Searching ........')
        new_search = Search(game, board, ply=ply)
        # new_search.search()


if __name__ == '__main__':
    # from board.Board import SetBoard, Boardmove

    board = ["none", "one", "none", "none", "none", "one", "none", "none",
             "one", "none", "none", "one", "one", "none",
             "one", "one", "one", "none", "none", "none", "one", "none", "two",
             "none", "none", "one", "none", "two",
             "none", "two", "none", "two", "two", "two", "none", "two", "two",
             "two", "two", "two", "none", "two",
             "two", "two", "none", "two", "two", "two", "two", "two"]
    # hh = SetBoard(560172527255552, 13835058055468269052)
    # my = Player(560172527255552 & (~ (1 << 32)))
    # opp = Player(13835058055468269052)

    my = Player(562399402786816)
    opp = Player(13835058055438925311)


    # my = Player(562399402786816 )
    # opp = Player(-4611686018270626305)

    # my = Player(-9222809671778172928)
    # opp = Player(- 4611686018404975361)

    # my = Player(my)
    # opp = Player(opp)
    b = Board(my, opp)

    game = Game()
    game.set_board(b)

    run_search(game, 3)

    move = Piece(sum((1 << i) for i in [24, 25, 26]))
    game.move(game.board, Board.from_move(game.board, move))
    game.move(game.board, Board.from_move(game.board, Piece(0)))

    run_search(game, 3)

    gg = game.board
    while gg:
        print(gg)
        gg = gg.prev

    print(0)


    # # ff = Search(b, ply=10)
    # move_log = []
    # # head = ff.board
    # # # ff = Search(bb, ply=5)
    # # print(3)
    # # head = bb
    # b_search = b
    # depth = 3
    #
    # new_search = Search(game, b_search, ply=depth)
    # # while not b_search.human_to_move():
    # #     new_search = Search(b_search, ply=depth)
    # #     move_log.append(new_search.move)
    # #     b_search = new_search.move
    # b_search = game.board
    # # print(b)
    # # for move in move_log:
    # #     b = Board.from_move(b, move)
    # #
    # # print(b)
    # # b = Board.from_move(b, Piece(0))
    # # print(b)
    #
    # # b = b_search
    # # b = Board.from_move(b, Piece(0))
    # move = sum((1 << i) for i in [24, 25, 26])
    # b1 = Board.from_move(b, Piece(move))
    # game.move(b, b1)
    # b2 = Board.from_move(b1, Piece(move))
    # game.move(b1, b2)
    # b3 = Board.from_move(b2, Piece(0))
    # game.move(b2, b3)
    #
    # # ff = Search(b, ply=10)
    # move_log = []
    # # head = ff.board
    # # # ff = Search(bb, ply=5)
    # # print(3)
    # # head = bb
    # b_search = b3
    # depth = 3
    # # new_search = Search(b_search, ply=depth)
    # while not b_search.human_to_move():
    #     new_search = Search(game, b_search, ply=depth)
    #     move_log.append(new_search.move)
    #     b_search = new_search.move
    #
    # print(b_search)
    # print(move_log)
