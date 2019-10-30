#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils import utils
from Utils.Bits import Bits
from engine.MoveGenerator import MoveGenerator
from .Evaluation import Evaluation


class Board:
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
    maxsize = 9223372036854775808
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

        self.reset(black_at_top, white_goes_first)

    def reset(self, black_at_top=True, white_goes_first=True):
        """Create Initial board or reset board"""
        self.previousPosition = None
        self.alreadyVisited = 0
        ImOnTop = (black_at_top ^ white_goes_first)  # Who is on Top
        if ImOnTop:
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
            if Board.collect_extra_statistics:
                Board.boardConsCount += 1
        else:
            captures = self.opponentPieces & move
            if captures != 0:
                self.child.opponentPieces = utils.NegBit(self.opponentPieces ^ captures)
                move ^= captures
                self.child.alreadyVisited = self.alreadyVisited | move
                self.child.myPieces = utils.NegBit(self.myPieces ^ move)
            else:
                self.child.opponentPieces = self.myPieces ^ move
                self.child.myPieces = utils.PosBit(self.opponentPieces)
                self.child.alreadyVisited = 0
        self.child.best_move = -1

    def set_principal_variation(self):
        """Setting Principal Variation search"""
        if Board.collect_extra_statistics:
            Board.pvChangeCount += 1
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
        Board.nodeCount += 1
        self.hasPrincipalVariation = False
        hash_value = None
        if self.mid_capture():
            eval_bool = Evaluation.evaluate(self, alpha, beta, depth)
            if (depth <= 0) and eval_bool:
                Board.leafCount += 1
                return
            hash_value = self.gethash()
            if hash_value in Board.movedict.keys():
                print('Already in move dict')
                stored_value = Board.movedict[hash_value]
                self.best_move = stored_value[2]
                stored_eval_type = stored_value[3]
                self.forced = stored_value[4]
                stored_eval = stored_value[5]
                if stored_eval_type == Board.eval_exact or (
                        stored_eval_type == Board.eval_upper_bound and stored_eval <= alpha) or (
                        stored_eval_type == Board.eval_lower_bound and stored_eval >= beta):
                    self.evaluation = stored_eval
                    if self.best_move >= 0 and (stored_eval >= alpha) and (stored_eval <= beta):
                        self.set_child(self.best_move)
                        self.child.hasPrincipalVariation = False
                        self.set_principal_variation()
                return

        if sequence_number != Board.sequence_number:
            print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return

        move_generator_is_set = False
        if self.best_move >= 0:
            move = self.best_move
        elif Board.iid and (depth >= Board.iid_limit):
            self.alpha_beta(depth - Board.iid_ply, alpha, beta, sequence_number)
            move = self.best_move
        else:
            self.set_move_generator()
            move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            self.forced = not (self.moveGenerator.hasMoreElements())
        first_move = move
        # Compute extensions
        new_depth = depth - Board.ply
        capture_extension = 0
        if self.forced:
            new_depth += Board.forced_move_extension
            if self.opponentPieces >= 0:
                capture_extension = Board.forced_endgame_capture - Board.forced_move_extension
            else:
                capture_extension = Board.forced_capture_extension - Board.forced_move_extension
        elif self.opponentPieces >= 0:
            capture_extension = Board.endgame_capture_extension
        elif self.myPieces < 0:
            capture_extension = Board.multiple_capture_extension

        # Set up alpha-beta parameters
        self.evaluation = -Board.maxsize
        eval_type = Board.eval_upper_bound
        pvs_beta = beta
        # Main alpha-beta loop
        while move >= 0:
            self.set_child(move)

            # if first move , check if it is already hashed
            if not self.child.mid_capture():  # Not midCapture
                self.child.alpha_beta(new_depth, -pvs_beta, -alpha, sequence_number)
                move_eval = -self.child.evaluation
                if pvs_beta <= move_eval < beta:
                    self.child.alpha_beta(new_depth, -beta, -alpha, sequence_number)
                    move_eval = -self.child.evaluation
                if (move_eval > self.evaluation) and (move == 0) and (not self.forced):
                    self.child.alpha_beta(new_depth + Board.early_pass_extension, -beta, -alpha, sequence_number)
                    move_eval = -self.child.evaluation

            # do this IF opponent piece not equal 0
            elif (self.child.opponentPieces & Bits.on_board) != 0:
                self.child.alpha_beta(new_depth + capture_extension, alpha, beta, sequence_number)
                move_eval = self.child.evaluation

            # opponent piece == 0 finish it
            else:
                self.evaluation = Bits.count(self.myPieces & Bits.on_board) * Board.won_position
                eval_type = Board.eval_exact
                self.best_move = move
                self.child.hasPrincipalVariation = False
                self.set_principal_variation()
                break

            if move_eval > self.evaluation:
                self.best_move = move
                self.evaluation = move_eval
                if move_eval > alpha:
                    alpha = move_eval
                    if move_eval >= beta:
                        eval_type = Board.eval_lower_bound
                        break  # fail high, prune search by breaking from loop
                    eval_type = Board.eval_exact
                    self.set_principal_variation()
            if self.forced:
                break
            if not move_generator_is_set:
                self.set_move_generator()
                move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            if move == first_move:
                move = self.moveGenerator.nextSet()
            if Board.pvs and (alpha < Board.decrementable) and (-alpha > -Board.decrementable):
                pvs_beta = alpha + 1

        if sequence_number != Board.sequence_number:
            return
        if self.evaluation > Board.decrementable:
            self.evaluation -= Board.ply_decrement
        elif self.evaluation < -Board.decrementable:
            self.evaluation += Board.ply_decrement
        if hash_value:
            print('Write to movedict')
            Board.movedict[hash_value] = (
            self.myPieces, self.opponentPieces, self.best_move, eval_type, self.forced, self.evaluation, depth)

    def __repr__(self):
        ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (self.myPieces, self.opponentPieces)
        board_pieces = utils.PiecesOnBoard(self.myPieces, self.opponentPieces)
        for i in range(5):
            ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
        return ff


class Boardmove(Board):
    def __init__(self, previousPosition, move):
        super().__init__()
        self.previousPosition = previousPosition
        captures = previousPosition.opponentPieces & move
        if captures != 0:
            self.opponentPieces = utils.NegBit(previousPosition.opponentPieces ^ captures)
            move ^= captures
            self.alreadyVisited = previousPosition.alreadyVisited | move
            self.myPieces = utils.NegBit(previousPosition.myPieces ^ move)
        else:
            self.opponentPieces, self.myPieces = previousPosition.myPieces ^ move, utils.PosBit(
                previousPosition.opponentPieces)
            self.alreadyVisited = 0
