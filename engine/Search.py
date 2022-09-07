import os
import sys
from wrapt_timeout_decorator import *
sys.path.append(os.path.realpath('..'))

from Utils.utils import *

from board.Board import Board
from board.Board import MoveGenerator
from engine.game import Game
import time


def current_milli_time():
    return time.time() * 1000


class Search:
    searchBound = 7200
    ASPIRATION_WINDOW = 50
    currentEval = 0

    def __init__(self, game, boardin, ply=3, time_max=3000):
        self.stop = False
        self.watcher = None
        self.firstMove = None
        self.board = boardin
        self.ply = ply
        self.move = None
        self.move_log = []
        self.game = game
        time.sleep(0)
        self.time_max = time_max

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
            move_ = newmg.nextSet()
            move = Board.from_move(board, move_)
        self.game.move(board, move)

    def abort(self):
        if logging:
            print("Position changed while searching, search aborted")
        Board.sequence_number += 1  # terminate currently running search

    def panic(self):
        Board.sequence_number += 1  # terminate currently running search
        if logging:
            print("Search timed out, making move without finishing search")
        self.make_board_move()

    def done(self):
        self.make_board_move()
        self.board.child = None
        self.board.PVar = None
        self.board.moveGenerator = None

    def run(self):
        if Game.must_pass(self.board):
            if logging:
                print('Forced pass')
            board = self.board
            new_board_move = Board.from_move(board, Piece(0))
            board.best_move = Piece(0)
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
            self.board.best_move = nextmove
            if logging:
                print("Forced move")
            self.done()
            return

        if Board.endgameDatabase is not None:
            self.set_board_move(self.board.PVar)
            self.done()
            return
        try:
            self.search()
            print('no Timeout Occured')
        except TimeoutError():
            # this will never be printed because the decorated function catches implicitly the TimeoutError !
            print('Timeout Occured')

    # @ timeout(3000)
    def search(self):
        depth = 1
        log_disabled = False
        previous_eval = 0
        self.move_log = []
        self.board.best_move = Piece(-1)
        Board.sequence_number += 1
        sequence_number = Board.sequence_number
        start_time = current_milli_time()
        while (self.ply == 0 or depth <= self.ply) and (current_milli_time()-
                                                        start_time < self.time_max):
            Board.nodeCount = Board.leafCount = 0
            if Board.collect_extra_statistics:
                Board.boardConsCount = Board.moveGenConsCount = 0
                Board.endgameEvalCount = Board.pvChangeCount = 0

            if Hash.collect_statistic_hash:
                Hash.hits = Hash.misses = Hash.shallow = Hash.badBound = 0

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
            # if (current_milli_time() - start_time) > self.time_max:
            #     new_board = Board.from_move(self.board,
            #                                 self.board.best_move)
            #     print(f'Time exceeded {depth}')
            #     self.set_board_move(new_board)
            #     self.done()
            #     return

            if Search.winning(previous_eval) and (
                    not Search.between(0, previous_eval, Search.currentEval)):
                Search.currentEval = previous_eval
            elif self.board.PVar is not None:
                # print('PVar', self.board.best_move)
                new_board = Board.from_move(self.board, self.board.best_move)
                self.set_board_move(new_board)
            if (not log_disabled) or (Search.currentEval != previous_eval):
                previous_eval = Search.currentEval
                if logging:
                    exec_time = current_milli_time() - start_time + 1
                    hash_stat = ''
                    if Hash.collect_statistic_hash:
                        total_hash = Hash.total_hash()
                        if total_hash == 0:
                            total_hash = 1
                        hits_rate = int((Hash.hits * 100) / total_hash)
                        max_rate = int(100 * (Hash.hits + Hash.shallow +
                                              Hash.badBound) / total_hash)
                        hash_stat = f', hash rate {hits_rate}%- {max_rate}%'
                    print(f'{depth} ply: {Search.currentEval / 100},'
                          f' {Board.nodeCount} '
                          f'nodes, {Board.leafCount} leaves, '
                          f'{int(Board.nodeCount / exec_time)}k nps {hash_stat}')
            if logging:
                self.board.print_PVar()
            if Search.winning(Search.currentEval) and (not log_disabled):
                print("Winning line found, searching for better win")
                log_disabled = True
            depth += 1
            # time.sleep(0.1)
        self.done()

    @staticmethod
    def winning(evals):
        return (evals < -Search.searchBound) or (evals > Search.searchBound)

    @staticmethod
    def between(a, b, c):
        """ ((a <= b <= c)  OR (c <= b <= a)) AND a != c"""
        return (a >= b) != (c >= b)


class SearchWatcher:
    def __init__(self, s, search_time):
        self.search = s
        self.search_time = search_time
        self.observing = False

    def set_search_time(self, t):
        self.search_time =  t

    def get_search_time(self, t):
        return self.search_time

    def start(self):
        self.run()

    def observe(self):
        self.observing = True
        self.search.game.addObserver(self)

    def run(self):
        self.observe()

    def update_board(self, game, board):
        if self.search.game != game:
            return
        if self.search.board == board:
            return
        self.search.abort()
        self.done()



def run_search(game, ply=3, maxtime=3000):
    step=1
    while True:
        board = game.get_board()
        if board.human_to_move():
            break
        if logging:
            print('\n Searching ........')
        print('\n Searching ........', [board.prev.best_move if
                                        board.prev else -1])
        start = current_milli_time()
        search = Search(game, board, ply=ply, time_max=maxtime)
        search.run()
        print(f'step: {step} took {current_milli_time()-start}')
        step += 1


if __name__ == '__main__':
    # from board.Board import SetBoard, Boardmove

    # board0 = ["none", "one", "none", "none", "none", "one", "none", "none",
    #           "one", "none", "none", "one", "one", "none",
    #           "one", "one", "one", "none", "none", "none", "one", "none", "two",
    #           "none", "none", "one", "none", "two",
    #           "none", "two", "none", "two", "two", "two", "none", "two", "two",
    #           "two", "two", "two", "none", "two",
    #           "two", "two", "none", "two", "two", "two", "two", "two"]
    #
    # board = ['none', 'none', 'none', 'none', 'none', 'none', 'none', 'one',
    #          'one',
    #          'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none',
    #          'none',
    #          'one', 'none', 'none', 'two', 'two', 'none', 'none', 'none',
    #          'none',
    #          'none', 'none', 'one', 'none', 'two', 'none', 'two', 'none',
    #          'none',
    #          'none', 'two', 'none', 'two', 'none', 'none', 'two', 'two', 'none',
    #          'none',
    #          'none', 'none', 'two', 'two']

    # board = ["zero", "one", "one", "one", "one", "one", "one", "one", "one",
    #      "one", "zero", "one", "one", "one", "one", "zero", "one", "one", "one", "one", "zero", "two", "one", "two", "one", "one", "two", "one", "two", "one", "zero", "two", "two", "two", "two", "zero", "two", "two", "two", "two", "zero", "two", "two", "two", "two", "zero", "two", "two", "two", "two"]
    #
    # my_pieces, opp_pieces = board_to_bit(board)
    # my = Player(my_pieces)
    #
    #
    # was_capture = False
    # opp = Player(opp_pieces | (int(was_capture) << 63) | (1 << 62))
    my = Player(544755571228672)
    opp = Player(4611686035886554367)

    b = Board(my, opp)
    game = Game()
    game.set_board(b)
    search = Search(game, b, ply=3, time_max=3000)
    search.run()

    print('first')

    # my = Player(457811502825472)
    # opp = Player(4611686018704605570)

    # board = Board(my, opp)
    # hh = SetBoard(560172527255552, 13835058055468269052)
    # my = Player(560172527255552 & (~ (1 << 32)))
    # opp = Player(13835058055468269052)

    # my = Player(562399402786816)
    # opp = Player(13835058055438925311)
    # my = Player(562261963833344)
    # opp = Player(-4611686018253881873)
    # my = Player(544789930967040)
    # opp = Player(-4611686018064073217)

    # my = Player(562399402786816 )
    # opp = Player(-4611686018270626305)

    # my = Player(-9222809671778172928)
    # opp = Player(- 4611686018404975361)

    # my = Player(my)
    # opp = Player(opp)
    b = Board(my, opp)
    print(b)
    game = Game()
    game.set_board(b)

    # run_search(game, 3)
    #
    # gg = game.board
    # moves = []
    # # find pointer head
    # head = gg
    # while head.prev:
    #     head = head.prev
    #
    # cur = head
    # first_move = True
    # while cur.next:
    #     if first_move:
    #         move_pos = (cur.best_move & cur.myPieces).to_pos(True) + 1
    #         moves.append((move_pos, [0]))
    #         first_move = False
    #     move_pos = (cur.best_move & cur.open).to_pos(True) + 1
    #     move_ = cur.best_move.all_one()
    #     moves.append((move_pos, move_))
    #     cur = cur.next
    #     if cur.best_move <= 0:
    #         break

    # while cur.next:
    #     # print(cur)
    #     if cur.prev:
    #         move_pos = (cur.prev.best_move & cur.myPieces).to_pos(True)
    #         move_ = cur.prev.best_move.all_one()
    #         moves.append((move_pos, move_))
    #     else:
    #         move_pos = (cur.best_move & cur.myPieces).to_pos(True)
    #         moves.append((move_pos, [0]))
    #     cur = cur.next

    # while gg:
    #     # if gg.was_shuffle():
    #     #     move_pos = (gg.prev.best_move & gg.oppPieces).to_pos(True)
    #     #     move_ = gg.prev.best_move.all_one()
    #     #     moves.insert(0, (move_pos, move_))
    #     #
    #     #     move_pos = (gg.prev.best_move & gg.prev.myPieces).to_pos(True)
    #     #     moves.insert(0, (move_pos, [0]))
    #     #     break
    #
    #     if not gg.human_to_move():
    #         if gg.prev:
    #             move_pos = (gg.prev.best_move & gg.myPieces).to_pos(True)
    #             move_ = gg.prev.best_move.all_one()
    #             moves.insert(0, (move_pos, move_))
    #         else:
    #             move_pos = (gg.best_move & gg.myPieces).to_pos(True)
    #             moves.insert(0, (move_pos, [0]))
    #
    #     gg = gg.prev
    # from flask import jsonify
    # fff = jsonify({'m': moves})

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
