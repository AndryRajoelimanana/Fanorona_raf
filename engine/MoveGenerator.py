#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:51:46 2019

@author: andry
"""

from Utils.Bits import Bits


class Move(object):
    def __init__(self, from_square, to_square):
        self.from_square = from_square
        self.to_square = to_square


class MoveGenerator(object):
    arbitraryMoveIndex = 0
    capture_forward = 0
    capture_backward = 1
    no_capture = 2
    pass_move = 3
    no_more_moves = 4

    def __init__(self, board):
        self.board = board
        self.reset(board)
        self.captureType = 3
        self.nextSetvalue = self.GeneratorNextSet()

    def reset(self, board):
        self.board = board
        self.moveSetIndex = -1
        self.set = 0
        self.madeCapture = False
        myPieces = board.myPieces
        self.nextSetvalue = self.GeneratorNextSet()

        if board.midCapture():
            move = myPieces ^ board.previousPosition.myPieces
            self.storedFrom = myPieces & move
            if (move & (move << Bits.shift_vertical) & Bits.on_board) != 0:
                move = (move << Bits.shift_vertical) | rshift(move, Bits.shift_vertical)
            elif (move & (move << Bits.shift_horizontal) & Bits.on_board) != 0:
                move = (move << Bits.shift_horizontal) | rshift(move, Bits.shift_horizontal)
            elif (move & (move << Bits.shift_slant) & Bits.on_board) != 0:
                move = (move << Bits.shift_slant) | rshift(move, Bits.shift_slant)
            else:
                move = (move << Bits.shift_backslant) | rshift(move, Bits.shift_backslant)
            self.storedTo = Bits.on_board & ~(move | myPieces | board.opponentPieces | board.alreadyVisited)
            return
        else:
            self.storedFrom = myPieces
            self.storedTo = Bits.on_board & ~(myPieces | board.opponentPieces)
            return

    def getmoves(self, from_square, to_square, movetype):
        return (from_square & rshift(to_square, movetype)) | (to_square & rshift(from_square, movetype))

    def nextSet(self):
        try:
            return next(self.nextSetvalue)
        except:
            return -1

    def GeneratorNextSet(self):
        sfrom = self.storedFrom
        sto = self.storedTo
        target = self.board.opponentPieces

        # vertical forward
        capture_type = MoveGenerator.capture_forward
        item = Bits.shift_vertical
        movesV = self.getmoves(sfrom, sto, item)
        set_ = (movesV & (target >> 2 * item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # horizontal forward
        item = Bits.shift_horizontal
        movesH = self.getmoves(sfrom, sto, item)
        set_ = (movesH & (target >> 2 * item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # Slant forward
        item = Bits.shift_slant
        sfrom &= Bits.diagonal
        self.storedFrom = sfrom
        movesS = self.getmoves(sfrom, sto, item)
        set_ = (movesS & (target >> 2 * item))
        if (set_ != 0):
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # Backslant forward
        item = Bits.shift_backslant
        movesB = self.getmoves(sfrom, sto, item)
        set_ = (movesB & (target >> 2 * item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # vertical backward
        item = Bits.shift_vertical
        capture_type = MoveGenerator.capture_backward
        set_ = (movesV & (target << item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # horizontal backward
        item = Bits.shift_horizontal
        set_ = (movesH & (target << item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # slant backward
        item = Bits.shift_slant
        set_ = (movesS & (target << item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # Backslant  backward
        item = Bits.shift_backslant
        set_ = (movesB & (target << item))
        if set_ != 0:
            shift = item
            made_capture = True
            yield self.nextElement(capture_type, shift, set_, made_capture)

        # Shuffle
        if self.board.midCapture():
            capture_type = MoveGenerator.no_more_moves
            set_ = 1
            return self.nextElement(capture_type, 0, set_, False)

        elif self.madeCapture:
            capture_type = MoveGenerator.no_more_moves
            return self.nextElement(capture_type, 0, set_, False)

        capture_type = MoveGenerator.no_capture
        set_ = movesV
        if set_ != 0:
            shift = Bits.shift_vertical
            yield self.nextElement(capture_type, shift, set_, False)

        set_ = movesH
        if set_ != 0:
            shift = Bits.shift_horizontal
            yield self.nextElement(capture_type, shift, set_, False)

        set_ = movesS
        if set_ != 0:
            shift = Bits.shift_slant
            yield self.nextElement(capture_type, shift, set_, False)

        set_ = movesB
        if set_ != 0:
            shift = Bits.shift_backslant
            yield self.nextElement(capture_type, shift, set_, False)

        capture_type = MoveGenerator.no_more_moves
        yield self.nextElement(capture_type, 0, set_, False)
        return

    def hasCapture(self):
        return (self.captureType == MoveGenerator.capture_forward) | (
                    self.captureType == MoveGenerator.capture_backward)

    def hasMoreElements(self):
        return (self.captureType != MoveGenerator.no_more_moves)

    def nextElement(self, captureType, shift, set_, madeCapture):

        self.captureType = captureType
        bit = set_
        bit &= -bit
        set_ ^= bit
        if captureType == MoveGenerator.capture_forward:
            retval = bit | (bit << shift)
            bit <<= 2 * shift
            while (bit & self.board.opponentPieces) != 0:
                retval |= bit
                bit <<= shift
            return retval
        elif captureType == MoveGenerator.capture_backward:
            retval = bit | (bit << shift)
            bit = rshift(bit, shift)
            while (bit & self.board.opponentPieces) != 0:
                retval |= bit
                bit = rshift(bit, shift)
            return retval
        elif captureType == MoveGenerator.no_capture:
            return bit | (bit << shift)
        elif captureType == MoveGenerator.pass_move:
            return 0
        elif captureType == MoveGenerator.no_more_moves:
            return -1

    @staticmethod
    def arbitraryMove(board):
        from board.Board import Boardmove
        i = MoveGenerator.arbitraryMoveIndex
        MoveGenerator.arbitraryMoveIndex += 1
        moveGenerator = MoveGenerator(board)
        movegen = moveGenerator.GeneratorNextSet()
        while (moveGenerator.hasMoreElements()):
            move = next(movegen)
            i -= 1
            if (i < 0):
                # print('arbitrary move = %i and capture type = %i'% (move, moveGenerator.captureType))
                newmove = Boardmove(board, move)
                return newmove
        MoveGenerator.arbitraryMoveIndex = 1
        newmg = MoveGenerator(board)
        move = newmg.nextSet()
        newmove = Boardmove(board, move)
        print('arbitrary move A =', move)
        return newmove



def rshift(val, n):
    # return (val % 0x10000000000000000) >> n
    return (val & 0xffffffffffffffff) >> n
    # return val >> n

