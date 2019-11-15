#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:51:46 2019

@author: andry
"""

from Utils.Bits import Bits
from Utils.utils import *


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
        self.capture_type = 3
        self.set = 0
        self.shift = None
        self.storedFrom = None
        self.storedTo = None
        self.made_capture = False
        self.reset(board)
        self.nextSetvalue = self.find_next_element()

    def reset(self, board):
        self.board = board
        self.made_capture = False
        myPieces = board.myPieces
        self.set = 0
        self.shift = None
        self.storedFrom = None
        self.storedTo = None
        self.nextSetvalue = self.find_next_element()

        # if mid-capture use the same moving piece for the next move else you can use any piece that can eat
        #
        # get moving piece
        if board.mid_capture():
            move = (myPieces & Bits.on_board) ^ (board.previousPosition.myPieces & Bits.on_board)
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

    def generate_next_set(self):
        try:
            return next(self.nextSetvalue)
        except:
            self.capture_type = MoveGenerator.no_more_moves
            return

    def find_next_element(self):
        sfrom = self.storedFrom
        sto = self.storedTo
        target = self.board.opponentPieces
        self.made_capture = False

        # vertical forward
        self.capture_type = MoveGenerator.capture_forward
        item = Bits.shift_vertical
        movesV = get_moves(sfrom, sto, item)
        set_ = (movesV & (target >> 2 * item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # horizontal forward
        item = Bits.shift_horizontal
        movesH = get_moves(sfrom, sto, item)
        set_ = (movesH & (target >> 2 * item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # Slant forward
        item = Bits.shift_slant
        sfrom &= Bits.diagonal
        self.storedFrom = sfrom
        movesS = get_moves(sfrom, sto, item)
        set_ = (movesS & (target >> 2 * item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # Backslant forward
        item = Bits.shift_backslant
        movesB = get_moves(sfrom, sto, item)
        set_ = (movesB & (target >> 2 * item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        self.capture_type = MoveGenerator.capture_backward
        # vertical backward
        item = Bits.shift_vertical
        set_ = (movesV & (target << item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # horizontal backward
        item = Bits.shift_horizontal
        set_ = (movesH & (target << item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # slant backward
        item = Bits.shift_slant
        set_ = (movesS & (target << item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # Backslant  backward
        item = Bits.shift_backslant
        set_ = (movesB & (target << item))
        if set_ != 0:
            self.shift = item
            self.made_capture = True
            self.set = set_
            yield

        # Shuffle
        #
        # No shuffle if mid capture
        if self.board.mid_capture():
            self.capture_type = MoveGenerator.pass_move
            self.set = 1
            yield
            self.capture_type = MoveGenerator.no_more_moves
            return

        # No shuffle if there is another move that is able to eat. You must eat
        elif self.made_capture:
            self.capture_type = MoveGenerator.no_more_moves
            yield
            return

        self.capture_type = MoveGenerator.no_capture
        set_ = movesV
        if set_ != 0:
            self.shift = Bits.shift_vertical
            self.set = set_
            yield

        set_ = movesH
        if set_ != 0:
            self.shift = Bits.shift_horizontal
            self.set = set_
            yield

        set_ = movesS
        if set_ != 0:
            self.shift = Bits.shift_slant
            self.set = set_
            yield

        set_ = movesB
        if set_ != 0:
            self.shift = Bits.shift_backslant
            self.set = set_
            yield

        self.capture_type = MoveGenerator.no_more_moves
        yield
        return

    def hasCapture(self):
        return (self.capture_type == MoveGenerator.capture_forward) | (
                self.capture_type == MoveGenerator.capture_backward)

    def hasMoreElements(self):
        if self.set == 0:
            self.generate_next_set()
        return self.capture_type != MoveGenerator.no_more_moves

    def nextSet(self):
        # get all pieces that can eat in a specific direction and return move for each piece (last bit first) 
        if self.set == 0:
            self.generate_next_set()

        if not self.hasMoreElements():
            return -1
        # get each set of moving piece, last bit comes first
        bit = Bits.last_bit(self.set)

        # remove last bit from self.set
        self.set ^= bit

        # get move value for each piece that can move
        if self.capture_type == MoveGenerator.capture_forward:
            move_value = bit | (bit << self.shift)
            bit <<= 2 * self.shift
            # get eaten pieces for each move
            while (bit & self.board.opponentPieces) != 0:
                move_value |= bit
                bit <<= self.shift
            return move_value
        elif self.capture_type == MoveGenerator.capture_backward:
            move_value = bit | (bit << self.shift)
            bit = rshift(bit, self.shift)
            while (bit & self.board.opponentPieces) != 0:
                move_value |= bit
                bit = rshift(bit, self.shift)
            return move_value
        elif self.capture_type == MoveGenerator.no_capture:
            return bit | (bit << self.shift)
        elif self.capture_type == MoveGenerator.pass_move:
            self.capture_type = MoveGenerator.no_more_moves
            return 0
        elif self.capture_type == MoveGenerator.no_more_moves:
            self.capture_type = MoveGenerator.no_more_moves
            return 0
        return -1

    @staticmethod
    def arbitraryMove(board):
        from board.Board import Boardmove
        i = MoveGenerator.arbitraryMoveIndex
        MoveGenerator.arbitraryMoveIndex += 1
        moveGenerator = MoveGenerator(board)
        while moveGenerator.hasMoreElements():
            move = moveGenerator.nextSet()
            i -= 1
            if i < 0:
                new_move = Boardmove(board, move)
                return new_move
        MoveGenerator.arbitraryMoveIndex = 1
        newmg = MoveGenerator(board)
        move = newmg.nextSet()
        new_move = Boardmove(board, move)
        return new_move
