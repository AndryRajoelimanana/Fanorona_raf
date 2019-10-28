#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils import utils
from Utils.Bits import Bits
from engine.MoveGenerator import MoveGenerator
from Board.Evaluation import Evaluation


class Board:
    # Principal Variation Search
    pvs = True

    # Internal Iterative Deepening
    iid = True
    iid_ply = 25
    iid_limit = 55

    # Board ply
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
    collect_extra_statistics = False
    sequence_number = 0
    leafCount = 0
    nodeCount = 0
    boardConsCount = 0
    moveGenConsCount = 0
    pvChangeCount = 0
    endgameDatabase = None
    maxsize =  9223372036854775808

    def __init__(self, black_at_top=True, white_goes_first=True):

        # Evaluation parameter
        self.evaluation = 0
        self.bestMove = -1

        # tree creation
        self.principalVariation = None
        self.hasPrincipalVariation = None
        self.child = None
        self.moveGenerator = None

        # Force move
        self.forced = False
        self.movedict = {}

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
    def mustPass(board):
        """Check if we must pass"""
        if not (board.midCapture()):
            return False
        mg = MoveGenerator(board)
        nextset = mg.nextSet()
        return nextset == 0

    def midCapture(self):
        """Check the captured bit position 64 : 2**64 """
        return (self.myPieces & Bits.captured) != 0

    def whiteToMove(self):
        """use bitmask Bits.is_white = 2**63"""
        return (self.myPieces & Bits.is_white) != 0

    def humanToMove(self):
        """use whiteToMove and HUMAN_PLAY_WHITE"""
        if self.whiteToMove():
            return self.HUMAN_PLAY_WHITE
        else:
            return self.HUMAN_PLAYS_BLACK

    def setMoveGenerator(self):
        """Setting move generator"""
        if self.moveGenerator is None:
            self.moveGenerator = MoveGenerator(self)
        else:
            self.moveGenerator.reset(self)

    def setChild(self, move):
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
        self.child.bestMove = -1

    def setPrincipalVariation(self):
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
            return hash((self.mypieces, self.opponentPieces))

        #    @property
        def alphaBeta(self, depth, alpha, beta, sequenceNumber):
            Board.nodeCount += 1
            self.hasPrincipalVariation = False
            if self.midCapture():
                evvv = Evaluation.evaluate(self, alpha, beta, depth)
                if ((depth <= 0) and evvv):
                    Board.leafCount += 1
                    return
                hash_value = self.gethash()
                if hash_value in self.movedict.keys():
                    bestMove = self.movedict[hash_value]
                    if (bestMove >= 0):
                        self.bestMove = bestMove
                        self.setChild(bestMove)
                        self.child.hasPrincipalVariation = False
                        self.setPrincipalVariation()
                    return

                    #            hashKey = Board.hash1.hashKey(self)
            #            # print(hashKey, self.bestMove, self.evaluation, alpha, beta)
            #            if (Board.hash1.getHash(self, hashKey, alpha, beta, depth)):
            #                if ((self.bestMove >= 0) and (self.evaluation >= alpha) and (self.evaluation <= beta)):
            #                    self.setChild(self.bestMove)
            #                    self.child.hasPrincipalVariation = False
            #                    self.setPrincipalVariation()
            #                    # print('Tato hash')
            #                return

            if (sequenceNumber != Board.sequence_number):
                print("Sequence number %s != %s" % (sequenceNumber, Board.sequence_number))
                return

            moveGeneratorIsSet = False
            if (self.bestMove >= 0):
                move = self.bestMove
            elif ((Board.iid) and (depth >= Board.iid_limit)):
                self.alphaBeta(depth - Board.iid_ply, alpha, beta, sequenceNumber)
                move = self.bestMove
            else:
                self.setMoveGenerator()
                moveGeneratorIsSet = True
                move = self.moveGenerator.nextSet()
                # print("Movegen: ",move, self.myPieces, self.opponentPieces)
                self.forced = not (self.moveGenerator.hasMoreElements())
            firstMove = move
            # Compute extensions
            newDepth = depth - Board.ply
            captureExtension = 0
            if (self.forced):
                newDepth += Board.forced_move_extension
                if (self.opponentPieces >= 0):
                    captureExtension = Board.forced_endgame_capture - Board.forced_move_extension
                else:
                    captureExtension = Board.forced_capture_extension - Board.forced_move_extension
            elif (self.opponentPieces >= 0):
                captureExtension = Board.endgame_capture_extension
            elif (self.myPieces < 0):
                captureExtension = Board.multiple_capture_extension

            # Set up alpha-beta parameters
            self.evaluation = -Board.maxsize
            evalType = Board.eval_upper_bound
            pvsBeta = beta
            # Main alpha-beta loop
            while (move >= 0):
                self.setChild(move)
                # print(move, newDepth)
                print("move = %s" % move)
                # if first move , check if it is already hashed

                if (self.child.myPieces >= 0):  # Not midCapture
                    self.child.alphaBeta(
                        newDepth, -pvsBeta, -alpha, sequenceNumber)
                    moveEval = -self.child.evaluation
                    if (moveEval >= pvsBeta) and (moveEval < beta):
                        self.child.alphaBeta(
                            newDepth, -beta, -alpha, sequenceNumber)
                        moveEval = -self.child.evaluation
                    if (moveEval > self.evaluation) and (move == 0) and (not (self.forced)):
                        self.child.alphaBeta(
                            newDepth + Board.early_pass_extension, -beta, -alpha, sequenceNumber)
                        moveEval = -self.child.evaluation

                # end hashed

                # do this IF opponent piece not equal 0

                elif ((self.child.opponentPieces & Bits.on_board) != 0):
                    self.child.alphaBeta(
                        newDepth + captureExtension, alpha, beta, sequenceNumber)
                    moveEval = self.child.evaluation

                # opponent piece == 0 finish it

                else:
                    self.evaluation = Bits.count(
                        self.myPieces & Bits.on_board) * Board.won_position
                    evalType = Board.eval_exact
                    self.bestMove = move
                    self.child.hasPrincipalVariation = False
                    self.setPrincipalVariation()
                    break

                # print("fff: ",newDepth,' ',move,' ',alpha,' ',beta," ",Board.nodeCount);
                # print("alphabeta: ", self.myPieces,' ',self.opponentPieces,' ',self.bestMove,' ',self.evaluation);

                if (moveEval > self.evaluation):
                    self.bestMove = move
                    self.evaluation = moveEval
                    if (moveEval > alpha):
                        alpha = moveEval
                        if (moveEval >= beta):
                            evalType = Board.eval_lower_bound
                            break  # fail high, prune search by breaking from loop
                        evalType = Board.eval_exact
                        self.setPrincipalVariation()
                if (self.forced):
                    break
                if not (moveGeneratorIsSet):
                    self.setMoveGenerator()
                    moveGeneratorIsSet = True
                # print("moveSetindex",self.moveGenerator.moveSetIndex)
                move = self.moveGenerator.nextSet()
                if (move == firstMove):
                    move = self.moveGenerator.nextSet()
                if (Board.pvs and (alpha < Board.decrementable) and (-alpha > -Board.decrementable)):
                    pvsBeta = alpha + 1

            if (sequenceNumber != Board.sequence_number):
                return
            if (self.evaluation > Board.decrementable):
                self.evaluation -= Board.ply_decrement
            elif (self.evaluation < -Board.decrementable):
                self.evaluation += Board.ply_decrement
            if (hashKey >= 0):
                Board.hash1.setHash(self, hashKey, evalType, depth)


    def __repr__(self):
        ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (self.myPieces, self.opponentPieces)
        board_pieces = utils.PiecesOnBoard(self.myPieces, self.opponentPieces)
        for i in range(5): ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
        return ff


class Boardmove(Board):
    def __init__(self, previousPosition, move):
        super().__init__()
        self.previousPosition = previousPosition
        captures = previousPosition.opponentPieces & move
        if (captures != 0):
            self.opponentPieces = utils.NegBit(previousPosition.opponentPieces ^ captures)
            move ^= captures
            self.alreadyVisited = previousPosition.alreadyVisited | move
            self.myPieces = utils.NegBit(previousPosition.myPieces ^ move)
        else:
            oppp = previousPosition.opponentPieces
            self.opponentPieces = previousPosition.myPieces ^ move
            self.myPieces = utils.PosBit(oppp)
            self.alreadyVisited = 0
