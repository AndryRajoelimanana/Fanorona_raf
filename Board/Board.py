#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils import utils
from Utils.Bits import Bits
from Utils.MoveGenerator import MoveGenerator



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
    sequenceNumber = 0
    leafCount = 0
    nodeCount = 0
    boardConsCount = 0
    moveGenConsCount = 0
    pvChangeCount = 0
    endgameDatabase = None
    maxsize = 2147483647

    def __init__(self, blackAtTop=True, whiteGoesFirst=True):

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

        self.blackAtTop = blackAtTop
        self.whiteGoesFirst = whiteGoesFirst
        self.HUMAN_PLAY_WHITE = True
        self.HUMAN_PLAYS_BLACK = not (self.HUMAN_PLAY_WHITE)

        self.reset(blackAtTop, whiteGoesFirst)

    def reset(self, blackAtTop=True, whiteGoesFirst=True):
        '''Create Initial board or reset board'''
        self.previousPosition = None
        self.alreadyVisited = 0
        ImOnTop = (blackAtTop ^ whiteGoesFirst)  # Who is on Top
        if ImOnTop:
            self.myPieces = Bits.initial_top
            self.opponentPieces = Bits.initial_bot
        else:
            self.myPieces = Bits.initial_bot
            self.opponentPieces = Bits.initial_top

        # Who goes first?
        if whiteGoesFirst:
            self.myPieces = self.myPieces | Bits.is_white  # bottom and white
        else:
            self.opponentPieces = self.opponentPieces | Bits.is_white

    @staticmethod
    def mustPass(board):
        '''Check if we must pass'''
        if not (board.midCapture()):
            return False
        mg = MoveGenerator(board)
        nextset = mg.nextSet()
        return (nextset == 0)

    def midCapture(self):
        '''Check the captured bit position 64 : 2**64 '''
        return (self.myPieces & Bits.captured) != 0

    def whiteToMove(self):
        '''use bitmask Bits.is_white = 2**63'''
        return (self.myPieces & Bits.is_white) != 0

    def humanToMove(self):
        '''use whiteToMove and HUMAN_PLAY_WHITE'''
        if (self.whiteToMove()):
            return self.HUMAN_PLAY_WHITE
        else:
            return self.HUMAN_PLAYS_BLACK

    def setMoveGenerator(self):
        '''Setting move generator'''
        if (self.moveGenerator == None):
            self.moveGenerator = MoveGenerator(self)
        else:
            self.moveGenerator.reset(self)

    def setChild(self, move):
        '''Setting child tree'''
        if self.child == None:
            self.child = Boardmove(self, move)
            if (Board.collect_extra_statistics):
                Board.boardConsCount += 1
        else:
            captures = self.opponentPieces & move
            if (captures != 0):
                self.child.opponentPieces = utils.NegBit(self.opponentPieces ^ captures)
                move ^= captures
                self.child.alreadyVisited = self.alreadyVisited | move
                self.child.myPieces = utils.NegBit(self.myPieces ^ move)
            else:
                self.child.opponentPieces = self.myPieces ^ move
                self.child.myPieces = utils.PosBit(self.opponentPieces)
                self.child.alreadyVisited = 0
        self.child.bestMove = -1;

    def setPrincipalVariation(self):
        '''Setting Principal Variation search'''
        if (Board.collect_extra_statistics):
            Board.pvChangeCount += 1
        if (self.principalVariation == None):
            self.principalVariation = self.child
            self.child = self.principalVariation.child
            if (self.child != None):
                self.child.previousPosition = self
        else:
            temp = self.child
            self.child = self.principalVariation
            self.principalVariation = temp
            self.child.child = self.principalVariation.child
            if (self.child.child != None):
                self.child.child.previousPosition = self.child
        self.principalVariation.child = None
        self.hasPrincipalVariation = True

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
