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

    def reset(self, board: BoardT):
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
            move = myPieces.val ^ board.prev.myPieces.val
            self.storedFrom = myPieces & move

            if (move & (move << Bits.shift_vertical)) != 0:
                move = p_move(move, Bits.shift_vertical)
            elif (move & (move << Bits.shift_horizontal)) != 0:
                move = p_move(move, Bits.shift_horizontal)
            elif (move & (move << Bits.shift_slant)) != 0:
                move = p_move(move, Bits.shift_slant)
            else:
                move = p_move(move, Bits.shift_backslant)
            self.storedTo = ~(move | myPieces | board.oppPieces | board.visited)
        else:
            self.storedFrom = myPieces
            self.storedTo = board.open

    def generate_next_set(self):
        try:
            return next(self.nextSetvalue)
        except:
            self.capture_type = MoveGenerator.no_more_moves
            return

    def find_next_element(self):
        sfrom = self.storedFrom.copy()
        sto = self.storedTo
        target = self.board.oppPieces
        made_capture = False
        set_ = None

        # forward capture
        capture_type = self.capture_forward
        for item in list_moves:
            if item in list_slant:
                moves = get_moves(sfrom & Bits.diagonal, sto, item)
            else:
                moves = get_moves(sfrom, sto, item)
            set_ = (moves & (target >> 2 * item))
            if set_ != 0:
                yield item, True, set_, capture_type

        # backward capture
        capture_type = self.capture_backward
        for item in list_moves:
            if item in list_slant:
                moves = get_moves(sfrom & Bits.diagonal, sto, item)
            else:
                moves = get_moves(sfrom, sto, item)
            set_ = (moves & (target << item))
            if set_ != 0:
                made_capture = True
                yield item, made_capture, set_, capture_type

        # Shuffle
        if self.board.mid_capture():
            return None, False, 1, self.pass_move

        # No shuffle if there is another move that is able to eat. You must eat
        elif made_capture:
            return None, False, set_, self.no_more_moves

        capture_type = self.no_capture
        for item in list_moves:
            if item in list_slant:
                moves = get_moves(sfrom & Bits.diagonal, sto, item)
            else:
                moves = get_moves(sfrom, sto, item)
            set_ = moves
            if set_ != 0:
                return item, made_capture, set_, capture_type

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
            while (bit & self.board.oppPieces) != 0:
                move_value |= bit
                bit <<= self.shift
            return move_value
        elif self.capture_type == MoveGenerator.capture_backward:
            move_value = bit | (bit << self.shift)
            bit = rshift(bit, self.shift)
            while (bit & self.board.oppPieces) != 0:
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
