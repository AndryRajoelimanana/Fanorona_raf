#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils.utils import *
from Utils import utils
from Utils.Bits import Bits
# from engine.MoveGenerator import MoveGenerator
from board.Evaluation import Evaluation
from typing import TypeVar

BoardT = TypeVar('BoardT', bound='Board')


class Board:
    # Principal Variation Search
    pvs = True

    # Internal Iterative Deepening
    iid = True
    iid_ply = 25
    iid_limit = 55

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

    def __init__(self, black_at_top: bool = True, white_goes_first: bool = True,
                 prev: BoardT = None, move: PiecesT = None):
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
        self.previousPosition = prev

        if prev and move:
            capture = prev.opponentPieces & move
            if capture:
                hh = prev.opponentPieces ^ capture
                self.opponentPieces: PiecesT = hh | Bits.captured
                move ^= capture
                self.alreadyVisited = prev.alreadyVisited | move
                self.my_pieces: PiecesT  = (prev.myPieces ^ move) | Bits.captured
            else:
                self.opponentPieces: PiecesT  = prev.my_pieces ^ move
                self.my_pieces: PiecesT  = prev.opponentPieces & ~Bits.captured
                self.alreadyVisited = 0
        else:
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
    def my_p(self) -> Pieces:
        return self.myPieces.on_board()

    @property
    def opp_p(self) -> Pieces:
        return self.opponentPieces.on_board()

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
        if Board.collect_extra_statistics:
            Board.pvChangeCount += 1
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
                self.child.opponentPieces = (
                                                        self.opponentPieces ^ captures) | Bits.captured
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

        if sequence_number != Board.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return

        move_generator_is_set = False
        if self.best_move >= 0:
            move = self.best_move
        elif Board.iid and (depth >= Board.iid_limit):
            self.alpha_beta(depth - Board.iid_ply, alpha, beta,
                            sequence_number)
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

        # set capture extension for
        #  - no more available move
        #  - was shuffle
        #  - mid - capture
        if self.forced:
            new_depth += Board.forced_move_extension
            # previous opponent move was a shuffle
            if self.was_shuffle():
                capture_extension = Board.forced_endgame_capture - \
                                    Board.forced_move_extension  # currently
                # 10 - 5
            else:
                capture_extension = Board.forced_capture_extension - \
                                    Board.forced_move_extension  # currently 10 - 5
        elif self.was_shuffle():
            capture_extension = Board.endgame_capture_extension  # currently 10
        elif self.mid_capture():
            capture_extension = Board.multiple_capture_extension  # currently 7

        # Set up alpha-beta parameters
        self.evaluation = -Board.maxsize
        eval_type = Board.eval_upper_bound  # assume upper bound until eval
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
                                          Board.early_pass_extension, -beta,
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
                eval_type = Board.eval_exact
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
            if Board.pvs and (alpha < Board.decrementable) and (-alpha >
                                                                  -Board.decrementable):
                pvs_beta = alpha + 1

        if sequence_number != Board.sequence_number:
            # print("Sequence number %s != %s" % (sequence_number, Board.sequence_number))
            return
        if self.evaluation > Board.decrementable:
            self.evaluation -= Board.ply_decrement
        elif self.evaluation < -Board.decrementable:
            self.evaluation += Board.ply_decrement
        if hash_value:
            Board.movedict[hash_value] = (
                self.myPieces, self.opponentPieces, self.best_move, eval_type,
                self.forced, self.evaluation, depth)

    def __repr__(self):
        bb = to64(self.my_p.val)[14:]
        bb1 = to64(self.opp_p.val)[14:]
        bb2 = ''
        for i, j in zip(bb, bb1):
            if i == '1':
                bb2 += 'o'
            elif j == '1':
                bb2 += 's'
            else:
                bb2 += '0'

        ff = ''
        for i in range(5):
            ff += '  '.join(bb2[i*10+1:(i+1)*10].replace('0', '.')) + '\n'
        return ff

    # def __repr__(self):
    #     ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (
    #         self.myPieces, self.opponentPieces)
    #     board_pieces = utils.PiecesOnBoard(self.myPieces, self.opponentPieces)
    #     for i in range(5):
    #         ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
    #     return ff


class Boardmove(Board):
    def __init__(self, previousPosition, move):
        super().__init__()
        self.previousPosition = previousPosition
        captures = previousPosition.opponentPieces & move
        if captures != 0:
            self.opponentPieces = (
                                              previousPosition.opponentPieces ^ captures) | Bits.captured
            move ^= captures
            self.alreadyVisited = previousPosition.alreadyVisited | move
            self.myPieces = (previousPosition.myPieces ^ move) | Bits.captured
        else:
            self.opponentPieces, self.myPieces = (
                                                             previousPosition.myPieces ^ move), (
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


class MoveGenerator(object):
    arbitraryMoveIndex = 0
    capture_forward = 0
    capture_backward = 1
    no_capture = 2
    pass_move = 3
    no_more_moves = 4

    def __init__(self, board: BoardT):
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

        # if mid-capture use the same moving piece for the next move else you
        # can use any piece that can eat
        #
        # get moving piece
        if board.mid_capture():
            move = (board.myPieces ^ board.previousPosition.myPieces).on_board()
            self.storedFrom = myPieces & move
            bb = move << Bits.shift_vertical
            if (move & (move << Bits.shift_vertical).o & Bits.on_board) != 0:
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
