#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:51:46 2019

@author: andry
"""

from Bits import Bits


class Move(object):
    def __init__(self, from_square, to_square):
        self.from_square = from_square
        self.to_square = to_square


class MoveGenerator(object):
    # class static variable
    arbitraryMoveIndex = 0
    capture_forward = 0
    capture_backward = 1
    no_capture = 2
    passa = 3
    no_more_moves = 4

    def __init__(self, board):
        self.board = board
        self.reset(board)
        self.captureType = 3

    def reset(self, board):
        self.board = board
        self.moveSetIndex = -1;
        self.set = 0
        self.madeCapture = False
        myPieces = board.myPieces

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
            # print(self.storedFrom, self.storedTo, self.set)
            return
        else:
            self.storedFrom = myPieces
            # print(myPieces , board.opponentPieces)
            self.storedTo = Bits.on_board & ~(myPieces | board.opponentPieces)
            return

    def getmoves(self, from_square, to_square, movetype):
        return (from_square & rshift(to_square, movetype)) | (to_square & rshift(from_square, movetype))

    def GeneratorNextSet(self):
        sfrom = self.storedFrom
        sto = self.storedTo
        target = self.board.opponentPieces

        # vertical forward
        captureType = MoveGenerator.capture_forward
        item = Bits.shift_vertical
        movesV = self.getmoves(sfrom, sto, item)
        set_ = (movesV & (target >> 2 * item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

        # horizontal forward
        item = Bits.shift_horizontal
        movesH = self.getmoves(sfrom, sto, item)
        set_ = (movesH & (target >> 2 * item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

        # Slant forward
        item = Bits.shift_slant
        sfrom &= Bits.diagonal
        self.storedFrom = sfrom;
        movesS = self.getmoves(sfrom, sto, item)
        set_ = (movesS & (target >> 2 * item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

        # Backslant forward
        item = Bits.shift_backslant
        movesB = self.getmoves(sfrom, sto, item)
        set_ = (movesB & (target >> 2 * item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

            # vertical backward
        item = Bits.shift_vertical
        captureType = MoveGenerator.capture_backward
        set_ = (movesV & (target << item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

            # horizontal backward
        item = Bits.shift_horizontal
        set_ = (movesH & (target << item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

            # slant backward
        item = Bits.shift_slant
        set_ = (movesS & (target << item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

            # Backslant  backward
        item = Bits.shift_backslant
        set_ = (movesB & (target << item))
        if (set_ != 0):
            shift = item
            madeCapture = True;
            yield self.nextElement(captureType, shift, set_, madeCapture)

            # Shuffle
        if (self.board.midCapture()):
            captureType = MoveGenerator.no_more_moves
            set_ = 1
            return self.nextElement(captureType, 0, set_, False)

        elif (self.madeCapture):
            captureType = MoveGenerator.no_more_moves
            return self.nextElement(captureType, 0, set_, False)

        captureType = MoveGenerator.no_capture
        set_ = movesV
        if (set_ != 0):
            shift = Bits.shift_vertical
            yield self.nextElement(captureType, shift, set_, False)

        set_ = movesH
        if (set_ != 0):
            shift = Bits.shift_horizontal
            yield self.nextElement(captureType, shift, set_, False)

        set_ = movesS
        if (set_ != 0):
            shift = Bits.shift_slant
            yield self.nextElement(captureType, shift, set_, False)

        set_ = movesB
        if (set_ != 0):
            shift = Bits.shift_backslant
            yield self.nextElement(captureType, shift, set_, False)

        captureType = MoveGenerator.no_more_moves
        yield self.nextElement(captureType, 0, set_, False)
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
        if (captureType == MoveGenerator.capture_forward):
            retval = bit | (bit << shift)
            bit <<= 2 * shift
            while (bit & self.board.opponentPieces) != 0:
                retval |= bit
                bit <<= shift
            return retval
        elif (captureType == MoveGenerator.capture_backward):
            retval = bit | (bit << shift)
            bit = rshift(bit, shift)
            while (bit & self.board.opponentPieces) != 0:
                retval |= bit
                bit = rshift(bit, shift)
            return retval
        elif captureType == MoveGenerator.no_capture:
            return bit | (bit << shift)
        elif captureType == MoveGenerator.passa:
            return 0
        elif captureType == MoveGenerator.no_more_moves:
            return -1

    @staticmethod
    def arbitraryMove(board):
        from Board import Board
        i = MoveGenerator.arbitraryMoveIndex
        MoveGenerator.arbitraryMoveIndex += 1
        moveGenerator = MoveGenerator(board)
        movegen = moveGenerator.GeneratorNextSet()
        while (moveGenerator.hasMoreElements()):
            move = next(movegen)
            i -= 1
            if (i < 0):
                # print('arbitrary move = %i and capture type = %i'% (move, moveGenerator.captureType))
                newboard = Board()
                newmove = newboard.Boardmove(board, move)
                return newmove
        MoveGenerator.arbitraryMoveIndex = 1
        newboard1 = Board()
        newmg = MoveGenerator(board).GeneratorNextSet()
        move = next(newmg)
        newmove = newboard1.Boardmove(board, move)
        print('arbitrary move A =', move)
        return newmove


class nextMoveGenerator(object):

    def __init__(self, movegen):
        self.movegen = movegen

    def __bool__(self):
        try:
            next(self.movegen.nextElement())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    def __len__(self):
        return self.bitboard.pseudo_legal_move_count()

    def __iter__(self):
        return self.movegen.nextElement()

    def __next__(self):
        return self.movegen.nextElement()

        # def __contains__(self, move):
    #    return self.bitboard.is_pseudo_legal(move)


def rshift(val, n):
    # return (val % 0x10000000000000000) >> n
    return (val & 0xffffffffffffffff) >> n
    # return val >> n

