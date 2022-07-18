#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils.utils import *
from Utils import utils
from Utils.Bits import Bits
from engine.MoveGenerator import MoveGenerator
from board.Evaluation import Evaluation
from typing import TypeVar
BoardT = TypeVar('BoardT', bound='Board')


class Board:
    # statistics gathering parameter
    collect_extra_statistics = True
    sequence_number = 0
    leafCount = 0
    nodeCount = 0
    boardConsCount = 0
    moveGenConsCount = 0
    pvChangeCount = 0
    endgameDatabase = None
    maxsize = (1 << 31) - 1
    movedict = {}

    def __init__(self, black_at_top=True, white_goes_first=True,
                 prev: BoardT = None, move=None):
        # Evaluation parameter
        self.evaluation = 0
        self.best_move = -1

        # tree creation
        self.principalVariation = None
        self.hasPrincipalVariation = None
        self.child = None
        self.moveGenerator = None

        # Force move
        self.forced = False
        self.HUMAN_PLAY_WHITE = True
        self.HUMAN_PLAYS_BLACK = not self.HUMAN_PLAY_WHITE

        if prev and move:
            self.previousPosition = prev
            capture = prev & move
            if capture:
                self.opponentPieces = (prev.opponentPieces ^ capture) | Bits.captured
                move ^= capture
                self.alreadyVisited = prev.alreadyVisited | move
                self.my_pieces = (prev.myPieces ^ move) | Bits.captured
            else:
                self.opponentPieces = prev.my_pieces ^ move
                self.my_pieces = prev.opponentPieces & ~Bits.captured
                self.alreadyVisited = 0
        else:
            self.previousPosition = None
            self.alreadyVisited = 0
            self.blackAtTop = black_at_top
            self.whiteGoesFirst = white_goes_first
            im_on_top = (black_at_top ^ white_goes_first)
            self.initial_position(im_on_top, white_goes_first)
            self.child = None

    def initial_position(self, im_on_top=True, white_goes_first=True):
        if im_on_top:
            self.myPieces = Pieces(Bits.initial_top)
            self.opponentPieces = Pieces(Bits.initial_bot)
        else:
            self.myPieces = Pieces(Bits.initial_bot)
            self.opponentPieces = Pieces(Bits.initial_top)

        self.myPieces |= (Bits.is_white & white_goes_first)
        self.opponentPieces |= (Bits.is_white & white_goes_first)

    def reset(self, black_at_top=True, white_goes_first=True):
        """Create Initial board or reset board"""
        self.previousPosition = None
        self.alreadyVisited = 0
        im_on_top = (black_at_top ^ white_goes_first)  # Who is on Top
        self.initial_position(im_on_top, white_goes_first)

    @property
    def my_p(self):
        return self.myPieces & Bits.on_board

    @property
    def opp_p(self):
        return self.opponentPieces & Bits.on_board

    @property
    def open(self):
        occupied = self.my_p | self.opp_p
        return ~occupied

    def __hash__(self):
        return hash((self.myPieces, self.opponentPieces))

    @staticmethod
    def must_pass(board):
        """Check if we must pass"""
        if not (board.mid_capture()):
            return False
        mg = MoveGenerator(board)
        next_set = mg.nextSet()
        return next_set == 0

    def mid_capture(self):
        """Check the captured bit position 64 : 2**64 """
        return (self.myPieces & Bits.captured) != 0

    def was_shuffle(self):
        """Check if opponent moved but didn't capture"""
        return (self.opponentPieces >> 63) == 0

    def was_pass(self):
        return (self.myPieces >> 63) ^ (self.opponentPieces >> 63)

    def white_to_move(self):
        """use bitmask Bits.is_white = 2**63"""
        return (self.myPieces & Bits.is_white) != 0

    def human_to_move(self):
        """use whiteToMove and HUMAN_PLAY_WHITE"""
        if self.white_to_move():
            return self.HUMAN_PLAY_WHITE
        else:
            return self.HUMAN_PLAYS_BLACK

    def gethash(self):
        return hash((self.myPieces, self.opponentPieces))

    def set_move_generator(self):
        """Setting move generator"""
        if self.moveGenerator is None:
            self.moveGenerator = MoveGenerator(self)
        else:
            self.moveGenerator.reset(self)

    def set_principal_variation(self):
        """Setting Principal Variation search"""
        if Board1.collect_extra_statistics:
            Board1.pvChangeCount += 1
        if self.principalVariation is None:
            self.principalVariation = self.child
            self.child = self.principalVariation.child
            if self.child is not None:
                self.child.previousPosition = self
        else:
            self.child, self.principalVariation = self.principalVariation, \
                                                  self.child
            self.child.child = self.principalVariation.child
            if self.child.child is not None:
                self.child.child.previousPosition = self.child
        self.principalVariation.child = None
        self.hasPrincipalVariation = True

    def set_child(self, move):
        """Setting child tree"""
        if self.child is None:
            self.child = Board(prev=self, move=move)
            if Board.collect_extra_statistics:
                Board.boardConsCount += 1
        else:
            captures = self.opponentPieces & move
            if captures:
                self.child.opponentPieces = (self.opponentPieces ^ captures) | Bits.captured
                move ^= captures
                self.child.alreadyVisited = self.alreadyVisited | move
                self.child.myPieces = (self.myPieces ^ move) | Bits.captured
            else:
                self.child.opponentPieces = self.myPieces ^ move
                self.child.myPieces = self.opponentPieces & ~Bits.captured
                self.child.alreadyVisited = 0
        self.child.best_move = -1

    def alpha_beta(self, depth, alpha, beta, sequence_number):
        Board.nodeCount += 1
        self.hasPrincipalVariation = False

        hash_value = hash(self)
        if not self.mid_capture():
            # is already evaluated?
            eval_bool = Evaluation.evaluate(self, alpha, beta, depth)
            if (depth <= 0) and eval_bool:
                Board.leafCount += 1
                return
            if utils.get_hash(Board, self, hash_value, alpha, beta, depth):
                if self.best_move >= 0 and (self.evaluation >= alpha) and (
                        self.evaluation <= beta):
                    self.set_child(self.best_move)
                    self.child.hasPrincipalVariation = False
                    self.set_principal_variation()
                return

        if sequence_number != Board1.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return

        move_generator_is_set = False
        if self.best_move >= 0:
            move = self.best_move
        elif Board1.iid and (depth >= Board1.iid_limit):
            self.alpha_beta(depth - Board1.iid_ply, alpha, beta,
                            sequence_number)
            move = self.best_move
        else:
            self.set_move_generator()
            move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            self.forced = not (self.moveGenerator.hasMoreElements())
        first_move = move
        # Compute extensions
        new_depth = depth - Board1.ply
        capture_extension = 0

        # set capture extension for
        #  - no more available move
        #  - was shuffle
        #  - mid - capture
        if self.forced:
            new_depth += Board1.forced_move_extension
            # previous opponent move was a shuffle
            if self.was_shuffle():
                capture_extension = Board1.forced_endgame_capture - \
                                    Board1.forced_move_extension  # currently
                # 10 - 5
            else:
                capture_extension = Board1.forced_capture_extension - \
                                    Board1.forced_move_extension  # currently 10 - 5
        elif self.was_shuffle():
            capture_extension = Board1.endgame_capture_extension  # currently 10
        elif self.mid_capture():
            capture_extension = Board1.multiple_capture_extension  # currently 7

        # Set up alpha-beta parameters
        self.evaluation = -Board1.maxsize
        eval_type = Board1.eval_upper_bound  # assume upper bound until eval
        # > alpha
        pvs_beta = beta

        # Main alpha-beta loop
        while move >= 0:
            self.set_child(move)
            # if first move , check if it is already hashed
            if not self.child.mid_capture():  # Not midCapture
                self.child.alpha_beta(new_depth, -pvs_beta, -alpha,
                                      sequence_number)
                move_eval = -self.child.evaluation
                if pvs_beta <= move_eval < beta:
                    self.child.alpha_beta(new_depth, -beta, -alpha,
                                          sequence_number)
                    move_eval = -self.child.evaluation
                if (move_eval > self.evaluation) and (move == 0) and (
                not self.forced):
                    self.child.alpha_beta(new_depth +
                                          Board1.early_pass_extension, -beta,
                                          -alpha, sequence_number)
                    move_eval = -self.child.evaluation

            # do this IF we still have opponent piece after the move
            elif (self.child.opponentPieces & Bits.on_board) != 0:
                self.child.alpha_beta(new_depth + capture_extension, alpha,
                                      beta, sequence_number)
                move_eval = self.child.evaluation

            # opponent piece == 0 finish it
            else:
                self.evaluation = Bits.count(
                    self.myPieces & Bits.on_board) * Board.won_position
                eval_type = Board1.eval_exact
                self.best_move = move
                self.child.hasPrincipalVariation = False
                self.set_principal_variation()
                break

            # How good is our move and compare it to alpha and beta (if eval > alpha => alpha = eval, if eval >=beta
            # => prune search)
            if move_eval > self.evaluation:
                self.best_move = move
                self.evaluation = move_eval
                if move_eval > alpha:
                    alpha = move_eval
                    if move_eval >= beta:
                        eval_type = Board1.eval_lower_bound
                        break  # fail high, prune search by breaking from loop
                    eval_type = Board1.eval_exact
                    self.set_principal_variation()
            if self.forced:
                break
            if not move_generator_is_set:
                self.set_move_generator()
                move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            if move == first_move:
                move = self.moveGenerator.nextSet()
            if Board1.pvs and (alpha < Board1.decrementable) and (-alpha >
                                                                  -Board1.decrementable):
                pvs_beta = alpha + 1

        if sequence_number != Board1.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return
        if self.evaluation > Board1.decrementable:
            self.evaluation -= Board1.ply_decrement
        elif self.evaluation < -Board1.decrementable:
            self.evaluation += Board1.ply_decrement
        if hash_value:
            Board1.movedict[hash_value] = (
                self.myPieces, self.opponentPieces, self.best_move, eval_type,
                self.forced, self.evaluation, depth)

    def __repr__(self):
        ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (
        self.myPieces, self.opponentPieces)
        board_pieces = utils.PiecesOnBoard(self.myPieces, self.opponentPieces)
        for i in range(5):
            ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
        return ff








class Board1:
    # Principal Variation Search
    pvs = True

    # Internal Iterative Deepening
    iid = True
    iid_ply = 25
    iid_limit = 55

    # board ply
    ply = 10
    ply_decrement = 1
    forced_move_extension = 5
    forced_capture_extension = 10
    endgame_capture_extension = 5
    forced_endgame_capture = 10
    multiple_capture_extension = 7
    early_pass_extension = 10
    won_position = 10000
    decrementable = 5000

    # Evaluation Type
    eval_upper_bound = 0
    eval_lower_bound = 1
    eval_exact = 2

    # statistics gathering parameter
    collect_extra_statistics = True
    sequence_number = 0
    leafCount = 0
    nodeCount = 0
    boardConsCount = 0
    moveGenConsCount = 0
    pvChangeCount = 0
    endgameDatabase = None
    maxsize = (1 << 31) - 1
    movedict = {}

    def __init__(self, black_at_top=True, white_goes_first=True):

        # Evaluation parameter
        self.evaluation = 0
        self.best_move = -1

        # tree creation
        self.principalVariation = None
        self.hasPrincipalVariation = None
        self.child = None
        self.moveGenerator = None

        # Force move
        self.forced = False

        self.blackAtTop = black_at_top
        self.whiteGoesFirst = white_goes_first
        self.HUMAN_PLAY_WHITE = True
        self.HUMAN_PLAYS_BLACK = not self.HUMAN_PLAY_WHITE

        self.previousPosition = None
        self.alreadyVisited = 0
        im_on_top = (black_at_top ^ white_goes_first)
        self.initial_position(im_on_top, white_goes_first)

    def reset(self, black_at_top=True, white_goes_first=True):
        """Create Initial board or reset board"""
        self.previousPosition = None
        self.alreadyVisited = 0
        im_on_top = (black_at_top ^ white_goes_first)  # Who is on Top
        self.initial_position(im_on_top, white_goes_first)

    def initial_position(self, im_on_top=True, white_goes_first=True):
        if im_on_top:
            self.myPieces = Bits.initial_top
            self.opponentPieces = Bits.initial_bot
        else:
            self.myPieces = Bits.initial_bot
            self.opponentPieces = Bits.initial_top

        # Who goes first?
        if white_goes_first:
            self.myPieces = self.myPieces | Bits.is_white  # bottom and white
        else:
            self.opponentPieces = self.opponentPieces | Bits.is_white

    @property
    def my_piecesb(self):
        return self.myPieces & Bits.on_board

    @property
    def opp_piecesb(self):
        return self.opponentPieces & Bits.on_board

    @property
    def count(self):
        return bin(self.my_piecesb).count('1')

    @property
    def open(self):
        occupied = self.my_piecesb | self.opp_piecesb
        return ~occupied

    @staticmethod
    def must_pass(board):
        """Check if we must pass"""
        if not (board.mid_capture()):
            return False
        mg = MoveGenerator(board)
        next_set = mg.nextSet()
        return next_set == 0

    def mid_capture(self):
        """Check the captured bit position 64 : 2**64 """
        return (self.myPieces & Bits.captured) != 0

    def was_shuffle(self):
        """Check if opponent moved but didn't capture"""
        return not (self.opponentPieces & Bits.captured)

    def white_to_move(self):
        """use bitmask Bits.is_white = 2**63"""
        return (self.myPieces & Bits.is_white) != 0

    def human_to_move(self):
        """use whiteToMove and HUMAN_PLAY_WHITE"""
        if self.white_to_move():
            return self.HUMAN_PLAY_WHITE
        else:
            return self.HUMAN_PLAYS_BLACK

    def set_move_generator(self):
        """Setting move generator"""
        if self.moveGenerator is None:
            self.moveGenerator = MoveGenerator(self)
        else:
            self.moveGenerator.reset(self)

    def set_child(self, move):
        """Setting child tree"""
        if self.child is None:
            self.child = Boardmove(self, move)
            if Board1.collect_extra_statistics:
                Board1.boardConsCount += 1
        else:
            captures = self.opponentPieces & move
            if captures != 0:
                self.child.opponentPieces = (self.opponentPieces ^ captures) | Bits.captured
                move ^= captures
                self.child.alreadyVisited = self.alreadyVisited | move
                self.child.myPieces = (self.myPieces ^ move) | Bits.captured
            else:
                self.child.opponentPieces, self.child.myPieces = (self.myPieces ^ move), (
                                                                         self.opponentPieces & ~Bits.captured)
                self.child.alreadyVisited = 0
        self.child.best_move = -1

    def set_principal_variation(self):
        """Setting Principal Variation search"""
        if Board1.collect_extra_statistics:
            Board1.pvChangeCount += 1
        if self.principalVariation is None:
            self.principalVariation = self.child
            self.child = self.principalVariation.child
            if self.child is not None:
                self.child.previousPosition = self
        else:
            temp = self.child
            self.child = self.principalVariation
            self.principalVariation = temp
            self.child.child = self.principalVariation.child
            if self.child.child is not None:
                self.child.child.previousPosition = self.child
        self.principalVariation.child = None
        self.hasPrincipalVariation = True

    def gethash(self):
        return hash((self.myPieces, self.opponentPieces))

    #    @property
    def alpha_beta(self, depth, alpha, beta, sequence_number):
        Board1.nodeCount += 1
        self.hasPrincipalVariation = False
        hash_value = self.gethash()
        if not self.mid_capture():
            eval_bool = Evaluation.evaluate(self, alpha, beta, depth)
            if (depth <= 0) and eval_bool:
                Board1.leafCount += 1
                return
            if utils.get_hash(Board1, self, hash_value, alpha, beta, depth):
                if self.best_move >= 0 and (self.evaluation >= alpha) and (
                        self.evaluation <= beta):
                    self.set_child(self.best_move)
                    self.child.hasPrincipalVariation = False
                    self.set_principal_variation()
                return

        if sequence_number != Board1.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return

        move_generator_is_set = False
        if self.best_move >= 0:
            move = self.best_move
        elif Board1.iid and (depth >= Board1.iid_limit):
            self.alpha_beta(depth - Board1.iid_ply, alpha, beta,
                            sequence_number)
            move = self.best_move
        else:
            self.set_move_generator()
            move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            self.forced = not (self.moveGenerator.hasMoreElements())
        first_move = move
        # Compute extensions
        new_depth = depth - Board1.ply
        capture_extension = 0

        # set capture extension for
        #  - no more available move
        #  - was shuffle
        #  - mid - capture
        if self.forced:
            new_depth += Board1.forced_move_extension
            # previous opponent move was a shuffle
            if self.was_shuffle():
                capture_extension = Board1.forced_endgame_capture - \
                                    Board1.forced_move_extension  # currently
                # 10 - 5
            else:
                capture_extension = Board1.forced_capture_extension - \
                                    Board1.forced_move_extension  # currently 10 - 5
        elif self.was_shuffle():
            capture_extension = Board1.endgame_capture_extension  # currently 10
        elif self.mid_capture():
            capture_extension = Board1.multiple_capture_extension  # currently 7

        # Set up alpha-beta parameters
        self.evaluation = -Board1.maxsize
        eval_type = Board1.eval_upper_bound  # assume upper bound until eval
        # > alpha
        pvs_beta = beta

        # Main alpha-beta loop
        while move >= 0:
            self.set_child(move)
            # if first move , check if it is already hashed
            if not self.child.mid_capture():  # Not midCapture
                self.child.alpha_beta(new_depth, -pvs_beta, -alpha,
                                      sequence_number)
                move_eval = -self.child.evaluation
                if pvs_beta <= move_eval < beta:
                    self.child.alpha_beta(new_depth, -beta, -alpha,
                                          sequence_number)
                    move_eval = -self.child.evaluation
                if (move_eval > self.evaluation) and (move == 0) and (
                not self.forced):
                    self.child.alpha_beta(new_depth +
                                          Board1.early_pass_extension, -beta,
                                          -alpha, sequence_number)
                    move_eval = -self.child.evaluation

            # do this IF we still have opponent piece after the move
            elif (self.child.opponentPieces & Bits.on_board) != 0:
                self.child.alpha_beta(new_depth + capture_extension, alpha,
                                      beta, sequence_number)
                move_eval = self.child.evaluation

            # opponent piece == 0 finish it
            else:
                self.evaluation = Bits.count(
                    self.myPieces & Bits.on_board) * Board.won_position
                eval_type = Board1.eval_exact
                self.best_move = move
                self.child.hasPrincipalVariation = False
                self.set_principal_variation()
                break

            # How good is our move and compare it to alpha and beta (if eval > alpha => alpha = eval, if eval >=beta
            # => prune search)
            if move_eval > self.evaluation:
                self.best_move = move
                self.evaluation = move_eval
                if move_eval > alpha:
                    alpha = move_eval
                    if move_eval >= beta:
                        eval_type = Board1.eval_lower_bound
                        break  # fail high, prune search by breaking from loop
                    eval_type = Board1.eval_exact
                    self.set_principal_variation()
            if self.forced:
                break
            if not move_generator_is_set:
                self.set_move_generator()
                move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            if move == first_move:
                move = self.moveGenerator.nextSet()
            if Board1.pvs and (alpha < Board1.decrementable) and (-alpha >
                                                                  -Board1.decrementable):
                pvs_beta = alpha + 1

        if sequence_number != Board1.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return
        if self.evaluation > Board1.decrementable:
            self.evaluation -= Board1.ply_decrement
        elif self.evaluation < -Board1.decrementable:
            self.evaluation += Board1.ply_decrement
        if hash_value:
            Board1.movedict[hash_value] = (
                self.myPieces, self.opponentPieces, self.best_move, eval_type,
                self.forced, self.evaluation, depth)

    def __repr__(self):
        ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (
        self.myPieces, self.opponentPieces)
        board_pieces = utils.PiecesOnBoard(self.myPieces, self.opponentPieces)
        for i in range(5):
            ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
        return ff


class Boardmove(Board1):
    def __init__(self, previousPosition, move):
        super().__init__()
        self.previousPosition = previousPosition
        captures = previousPosition.opponentPieces & move
        if captures != 0:
            self.opponentPieces = (previousPosition.opponentPieces ^ captures) | Bits.captured
            move ^= captures
            self.alreadyVisited = previousPosition.alreadyVisited | move
            self.myPieces = (previousPosition.myPieces ^ move) | Bits.captured
        else:
            self.opponentPieces, self.myPieces = (previousPosition.myPieces ^ move), (
                                                         previousPosition.opponentPieces & ~Bits.captured)
            self.alreadyVisited = 0


class SetBoard(Board):
    def __init__(self, my_pieces=Bits.initial_top, opp_pieces=Bits.initial_bot,
                 was_capture=True):
        super().__init__()
        self.myPieces = Pieces(my_pieces)
        self.opponentPieces = Pieces(opp_pieces | Bits.is_white)
        if was_capture:
            self.opponentPieces |= Bits.captured


if __name__ == '__main__':
    board = ["none", "one", "none", "none", "none", "one", "none", "none",
             "one", "none", "none", "one", "one", "none",
             "one", "one", "one", "none", "none", "none", "one", "none", "two",
             "none", "none", "one", "none", "two",
             "none", "two", "none", "two", "two", "two", "none", "two", "two",
             "two", "two", "two", "none", "two",
             "two", "two", "none", "two", "two", "two", "two", "two"]
    my_pieces, opp_pieces = utils.board_to_bit(board)
    print(my_pieces, opp_pieces)
    hh = SetBoard(4611686018596683196, 9223927819925454848)
    hh.alpha_beta(0, -2147483647, -640, 0)
    # print(hh.best_move, hh.evaluation)
    print(0)