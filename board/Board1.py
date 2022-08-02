#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:44:23 2019

@author: andry
"""

from Utils.utils1 import *
# from Utils import utils
from Utils.Bits import Bits
from Utils.configs import *
# from engine.MoveGenerator import MoveGenerator
from board.Evaluation1 import Evaluation
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

    # Internal Iterative Deepening
    iid = True
    iid_ply = 25
    iid_limit = 55

    ply = 10
    ply_decrement = 1

    # board ply
    forced_move_extension = 5
    forced_capture_extension = 10
    endgame_capture_extension = 5
    forced_endgame_capture = 10
    multiple_capture_extension = 7
    early_pass_extension = 10

    # Evaluation Type
    eval_upper_bound = 0
    eval_lower_bound = 1
    eval_exact = 2

    won_position = 10000
    decrementable = 5000

    # Principal Variation Search
    pvs = True
    hash = Hash()

    def __init__(self, my_pieces: Player, opp_pieces: Player,
                 prev: BoardT = None, visited: int = 0):
        self.myPieces = my_pieces
        self.oppPieces = opp_pieces
        self.prev = prev
        self.visited = visited

        # Evaluation parameter
        self.evaluation = -Board.maxsize
        self.best_move = Piece(-1)

        # tree creation
        self.PVar = None
        self.hasPVar = None
        self.child = None
        self.moveGenerator = None

        # Force move
        self.forced = False
        self.HUMAN_PLAY_WHITE = True
        self.HUMAN_PLAYS_BLACK = not self.HUMAN_PLAY_WHITE

        # debug = True
        self.attacking = None
        self.attackingPieces = None
        self.defendingPieces = None
        self.attackingActivity = None
        self.defendingActivity = None
        self.safeForDefense = None
        self.attackingTrapped = None
        self.stuckDefenders = None
        self.defendingTrapped = None
        self.move_generator_is_set = False

    @classmethod
    def initial_board(cls, black_at_top: bool = True,
                      white_goes_first: bool = True):
        im_on_top = (black_at_top ^ white_goes_first)
        if im_on_top:
            myPieces = Player(Bits.initial_top)
            oppPieces = Player(Bits.initial_bot)

        else:
            myPieces = Player(Bits.initial_bot)
            oppPieces = Player(Bits.initial_top)

        # Who goes first?
        if white_goes_first:
            myPieces = myPieces | Bits.is_white  # bottom and white
        else:
            oppPieces = oppPieces | Bits.is_white

        return cls(myPieces, oppPieces)

    @classmethod
    def from_move(cls, prev: BoardT, move: PieceT):
        # sourcery skip: use-named-expression
        capture = prev.oppPieces & move
        if capture.val != 0:
            oppPieces = prev.oppPieces ^ capture
            move = move ^ capture
            visited = prev.visited | move.val
            myPieces = prev.myPieces ^ move
            oppPieces.captured = True
            myPieces.captured = True
        else:
            oppPieces = prev.myPieces ^ move
            myPieces = prev.oppPieces ^ 0
            myPieces.captured = False
            visited = 0
        return cls(myPieces, oppPieces, prev, visited)

    # def from_move(self, prev: BoardT, move: PieceT):
    #     # sourcery skip: use-named-expression
    #     self.prev = prev
    #     capture = prev.oppPieces & move
    #     if capture.val != 0:
    #         self.oppPieces = prev.oppPieces ^ capture
    #         self.oppPieces.captured = True
    #         move = move ^ capture
    #         self.visited = prev.visited | move.val
    #         self.myPieces = prev.myPieces ^ move
    #         self.myPieces.captured = True
    #     else:
    #         self.oppPieces = prev.myPieces ^ move
    #         self.myPieces = prev.oppPieces
    #         self.myPieces.captured = False
    #         self.visited = 0

    @classmethod
    def from_ints(cls, my=Bits.initial_top, opp=Bits.initial_bot):
        myPieces = Player(my)
        oppPieces = Player(opp)
        return cls(myPieces, oppPieces)

    def reset(self, black_at_top=True, white_goes_first=True):
        """Create Initial board or reset board"""
        self.initial_board(black_at_top, white_goes_first)

    @property
    def open(self):
        occupied = self.myPieces | self.oppPieces
        return Bits.on_board & ~occupied

    def __hash__(self):
        # if isinstance(self.myPieces.value, Piece):
        #    print(0)
        return hash((self.myPieces.value, self.oppPieces.value))
        # n = self.myPieces.repr * -7417322830067466543 + \
        #        self.oppPieces.repr * -5499926718330407624
        # return rshift(n, 64 - 15)
        # return n

    @staticmethod
    def must_pass(board):
        """Check if we must pass"""
        if not (board.mid_capture()):
            return False
        mg = MoveGenerator(board)
        next_set = mg.nextSet()
        return next_set == 0

    @staticmethod
    def attack(mine, open_board):
        me = mine & Bits.on_board
        open_board = open_board & Bits.on_board

        unsafe = Piece(0)
        for i in [10, 1]:
            moves = get_moves(me, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        for i in [11, 9]:
            moves = get_moves(me & Bits.diagonal, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        return Piece(unsafe.val)

    def my_capture(self):
        return Piece((self.my_attack() & self.oppPieces).val)

    def opp_capture(self):
        return Piece((self.opp_attack() & self.myPieces).val)

    def my_attack(self):
        return Piece(self.attack(self.myPieces, self.open).val)

    def opp_attack(self):
        return Piece(self.attack(self.oppPieces, self.open).val)

    def my_safemove(self):
        return Piece((self.open & ~self.opp_attack()).val)

    def opp_safemove(self):
        return Piece((self.open & ~self.my_attack()).val)

    def my_activity(self):
        return Piece(self.myPieces.activity(self.my_safemove()).val)

    def opp_activity(self):
        return Piece(self.oppPieces.activity(self.opp_safemove()).val)

    def control(self):
        opp_pieces = self.oppPieces
        my_pieces = self.myPieces
        return opp_pieces.control() - my_pieces.control() + \
               opp_pieces.control('center') - my_pieces.control(
            'center') + opp_pieces.control('right') - my_pieces.control(
            'right')

    def find_side(self):
        my_activity = self.my_activity()
        opp_activity = self.opp_activity()
        if my_activity.val > opp_activity.val:
            self.attacking = True
            self.attackingPieces = self.myPieces
            self.defendingPieces = self.oppPieces
            self.attackingActivity = self.my_activity().count
            self.defendingActivity = self.opp_activity().count
            self.safeForDefense = self.opp_safemove()
            self.stuckDefenders = self.defendingPieces & ~self.opp_activity()
        else:
            self.attacking = False
            self.attackingPieces = self.oppPieces
            self.defendingPieces = self.myPieces
            self.attackingActivity = self.opp_activity().count
            self.defendingActivity = self.my_activity().count
            self.safeForDefense = self.my_safemove()
            self.stuckDefenders = self.defendingPieces & ~self.my_activity()

        self.attackingTrapped = self.attackingPieces.count - \
                                self.attackingActivity
        self.defendingTrapped = self.defendingPieces.count - \
                                self.defendingActivity

    def mid_capture(self):
        """Check the captured bit position 64 : 2**64 """
        return self.myPieces.captured

    def was_shuffle(self):
        """Check if opponent moved but didn't capture"""
        return not self.oppPieces.captured

    def was_pass(self):
        return self.myPieces.captured ^ self.oppPieces.captured
        # return (self.prev.myPieces.val == self.oppPieces.val) and (
        #     not self.oppPieces.captured)

    def white_to_move(self):
        """use bitmask Bits.is_white = 2**63"""
        return self.myPieces.is_white

    def human_to_move(self):
        """use whiteToMove and HUMAN_PLAY_WHITE"""
        if self.white_to_move():
            return self.HUMAN_PLAY_WHITE
        else:
            return self.HUMAN_PLAYS_BLACK

    def from_to(self, first_move=True):
        if self.was_pass():
            if first_move:
                print('pass', end=' ')
            return True
        prev = self.prev
        captures = prev.oppPieces & self.open
        from_ = prev.myPieces & self.open
        to_ = ~self.open & prev.open
        if from_.count > 1 or to_.count > 1:
            print(' ', end='')
            return False
        if from_.count == 0 or to_.count == 0:
            print(' ', end='')
            return True

        if not first_move and not prev.mid_capture():
            print(' ', end='')
            first_move = True
        if first_move:
            print(f'{from_.to_pos()}', end="")
        if captures == 0:
            print('-', end='')
        else:
            near_start = from_
            near_start |= p_move(near_start, 10)
            near_start |= p_move(near_start, 1)
            print(f'{"<" if (near_start & captures) != 0 else ">"}', end='')
        print(f'{to_.to_pos()}', end="")
        return True

    def print_PVar(self):
        pvar = self.PVar
        first_move = True
        print('  PV: ', end='')
        while pvar and pvar.from_to(first_move):
            pvar = pvar.PVar
            first_move = False
        print(' ')

    def gethash(self):
        return hash((self.myPieces.val, self.oppPieces.val))

    def set_move_generator(self):
        """Setting move generator"""
        if self.moveGenerator is None:
            self.moveGenerator = MoveGenerator(self)
        else:
            self.moveGenerator.reset(self)
        self.move_generator_is_set = True

    def set_principal_variation(self):
        """Setting Principal Variation search"""
        if Board.collect_extra_statistics:
            Board.pvChangeCount += 1
        if self.PVar is None:
            self.PVar = self.child
            self.child = self.PVar.child
            if self.child is not None:
                self.child.prev = self
        else:
            self.child, self.PVar = self.PVar, self.child
            self.child.child = self.PVar.child
            if self.child.child is not None:
                self.child.child.prev = self.child
        self.PVar.child = None
        self.hasPVar = True

    def set_child(self, move):
        """Setting child tree"""
        if self.child is None:
            self.child = Board.from_move(self, move)
            if Board.collect_extra_statistics:
                Board.boardConsCount += 1
        else:
            capture = self.oppPieces & move
            if capture.val != 0:
                self.child.oppPieces = self.oppPieces ^ capture
                self.child.oppPieces.captured = True
                move = move ^ capture
                self.child.visited = self.visited | move.val
                self.child.myPieces = self.myPieces ^ move
                self.child.myPieces.captured = True
            else:
                self.child.oppPieces = self.myPieces ^ move
                self.child.myPieces = self.oppPieces ^ 0
                self.child.myPieces.captured = False
                # self.child.oppPieces.captured = False
                self.child.visited = 0
        self.child.best_move = Piece(-1)

    def compute_capture_extension(self, depth):
        new_depth = depth - Board.ply
        capture_extension = 0

        # set capture extension for
        #  - no more available move
        #  - was shuffle
        #  - mid - capture
        if self.forced:
            if debug:
                print('Forced')
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
            if debug:
                print('shuffle')
            capture_extension = Board.endgame_capture_extension  # currently 10
        elif self.mid_capture():
            if debug:
                print('midcapture')
            capture_extension = Board.multiple_capture_extension  # currently 7
        return capture_extension, new_depth

    def find_firstmove(self, depth, alpha, beta, sequence_number):
        if self.best_move >= 0:
            move = self.best_move
            if debug:
                print(f"First bestmove selected:{move.val}")
        elif Board.iid and (depth >= Board.iid_limit):
            self.alpha_beta(depth - Board.iid_ply, alpha, beta,
                            sequence_number)
            move = self.best_move
            if debug:
                print(f"First iid move selected:{move.val}")
        else:
            self.set_move_generator()
            self.move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            self.forced = not (self.moveGenerator.hasMoreElements())
            if debug:
                print(f"First newGenerator move selected:{move.val} "
                      f"{'true' if self.forced else 'false'}")
        return move

    def was_evaluated(self, alpha, beta, depth):
        eval_bool = Evaluation.evaluate(self, alpha, beta, depth)
        if eval_bool is not None:
            self.evaluation = eval_bool
            if depth <= 0:
                Board.leafCount += 1
                if debug:
                    print("Time for leaf evaluation")
                return True
        hash_value = hash(self)
        if self.hash.get_hash(self, hash_value, alpha, beta, depth):
            return True
        return False

    def alpha_beta(self, depth, alpha, beta, sequence_number):
        if debug:
            print('  \n  ')
        Board.nodeCount += 1
        self.hasPVar = False
        if debug:
            print(f'alphabeta: {self.myPieces.repr} {self.oppPieces.repr} {depth} '
                  f' {alpha} {beta}')

        if not self.mid_capture() and self.was_evaluated(alpha, beta, depth):
            return

        # finish when sequence_number != Board sequence_number
        if sequence_number != Board.sequence_number:
            return

        # Find first move to be search
        self.move_generator_is_set = False

        move = self.find_firstmove(depth, alpha, beta, sequence_number)
        first_move = move

        # Compute extensions
        capture_extension, new_depth = self.compute_capture_extension(depth)

        # Set up alpha-beta parameters
        self.evaluation = -Board.maxsize
        eval_type = Board.eval_upper_bound  # assume upper bound until eval
        # > alpha
        pvs_beta = beta

        # Main alpha-beta loop
        while move >= 0:
            self.set_child(move)
            if debug:
                print(f'move: {move.val} {depth} {new_depth}')
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
                    dpth = new_depth + Board.early_pass_extension
                    self.child.alpha_beta(dpth, -beta, -alpha, sequence_number)
                    move_eval = -self.child.evaluation
            # do this IF we still have opponent piece after the move
            elif self.child.oppPieces != 0:
                dpth = new_depth + capture_extension
                self.child.alpha_beta(dpth, alpha, beta, sequence_number)
                move_eval = self.child.evaluation

            # opponent piece == 0 finish it
            else:
                # all pieces captured, fail high but hash exact eval
                self.evaluation = self.myPieces.count * Board.won_position
                eval_type = Board.eval_exact
                self.best_move = move
                self.child.hasPVar = False
                self.set_principal_variation()
                if debug:
                    print("WON position")
                break

            # How good is our move and compare it to alpha and beta
            # (if eval > alpha => alpha = eval, if eval >=beta
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
            if not self.move_generator_is_set:
                self.set_move_generator()
                self.move_generator_is_set = True
            move = self.moveGenerator.nextSet()
            if move == first_move:
                move = self.moveGenerator.nextSet()
            brd_decr = Board.decrementable
            if Board.pvs and (alpha < brd_decr) and (-alpha > -brd_decr):
                pvs_beta = alpha + 1

        if debug:
            print(f'BestMove:{self.best_move.val} {self.evaluation} '
                  f'{depth} {new_depth}')

        if sequence_number != Board.sequence_number:
            return
        if self.evaluation > Board.decrementable:
            self.evaluation -= Board.ply_decrement
        elif self.evaluation < -Board.decrementable:
            self.evaluation += Board.ply_decrement

        self.hash.set_hash(self, eval_type, depth)

        if debug:
            print(f'evaluation final: {self.evaluation}  BestMove: '
                  f'{self.best_move.val}  depth: {depth}')

    def __repr__(self):
        bb = to64(self.myPieces.val)[14:]
        bb1 = to64(self.oppPieces.val)[14:]
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
            ff += '  '.join(
                bb2[i * 10 + 1:(i + 1) * 10].replace('0', '.')) + '\n'
        return ff


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
        self.set = None
        self.shift = None
        self.storedFrom = Piece(0)
        self.storedTo = Piece(0)
        self.nextSetvalue = self.find_next_element()
        self.reset(board)

    def reset(self, board: BoardT):
        self.board = board
        myPieces = board.myPieces
        self.set = 0
        self.shift = None
        self.nextSetvalue = self.find_next_element()

        # if mid-capture use the same moving piece for the next move else you can use any piece that can eat
        #
        # get moving piece
        if board.mid_capture():
            move = myPieces.value ^ board.prev.myPieces.value
            self.storedFrom = myPieces & move

            if (move & (move << Bits.shift_vertical)) != 0:
                move = p_move(move, Bits.shift_vertical)
            elif (move & (move << Bits.shift_horizontal)) != 0:
                move = p_move(move, Bits.shift_horizontal)
            elif (move & (move << Bits.shift_slant)) != 0:
                move = p_move(move, Bits.shift_slant)
            else:
                move = p_move(move, Bits.shift_backslant)
            self.storedTo = Bits.on_board & ~(move | myPieces |
                                              board.oppPieces | board.visited)
        else:
            self.storedFrom = myPieces
            self.storedTo = board.open

    def generate_next_set(self):
        try:
            item, made_capture, set_, capture_type = next(self.nextSetvalue)
            # self.shift = item
            # self.made_capture = made_capture
            # self.set = set_
            self.capture_type = capture_type
        except Exception:
            self.capture_type = self.no_more_moves

    def find_next_element(self):
        no_more_move = False
        sfrom = self.storedFrom
        # if isinstance(self.storedTo, Piece):
        #    self.storedTo = self.storedTo.val
        sto = self.storedTo
        target = self.board.oppPieces.val
        made_capture = False
        set_ = None

        movesV = get_moves(sfrom, sto, 10)
        movesH = get_moves(sfrom, sto, 1)
        # self.storedFrom &= Bits.diagonal
        movesS = get_moves(sfrom & Bits.diagonal, sto, 11)
        movesB = get_moves(sfrom & Bits.diagonal, sto, 9)

        # forward capture
        for move, item in zip([movesV, movesH, movesS, movesB], [10, 1, 11, 9]):
            capture_type = self.capture_forward
            set_ = move & (target >> (2 * item))
            if set_ != 0:
                self.set = set_
                self.shift = item
                made_capture = True
                yield item, True, set_, capture_type

        # backward capture
        for move, item in zip([movesV, movesH, movesS, movesB], [10, 1, 11, 9]):
            capture_type = self.capture_backward
            set_ = move & (target << item)
            if set_ != 0:
                self.set = set_
                self.shift = item
                made_capture = True
                yield item, True, set_, capture_type

        # Shuffle
        # illegal to shuffle
        if self.board.mid_capture():
            self.set = Piece(1)
            no_more_move = True
            yield None, False, Piece(1), self.pass_move

        # No shuffle if there is another move that is able to eat. You must eat
        elif made_capture:
            no_more_move = True

        if not no_more_move:
            capture_type = self.no_capture
            for move, item in zip([movesV, movesH, movesS, movesB],
                                  [10, 1, 11, 9]):
                set_ = move
                if set_ != 0:
                    self.set = set_
                    self.shift = item
                    yield item, made_capture, set_, capture_type
        return None, False, set_, self.no_more_moves

    def hasCapture(self):
        if self.set == 0:
            self.generate_next_set()
        return (self.capture_type == MoveGenerator.capture_forward) | (
                self.capture_type == MoveGenerator.capture_backward)

    def hasMoreElements(self):
        if self.set == 0:
            self.generate_next_set()
        return self.capture_type != MoveGenerator.no_more_moves

    def nextSet(self):
        # get all pieces that can eat in a specific direction and return move
        # for each piece (last bit first)
        if self.set == 0:
            self.generate_next_set()

        if not self.hasMoreElements():
            return Piece(-1)
        # get each set of moving piece, last bit comes first
        bit = Bits.last_bit(self.set)

        # remove last bit from self.set
        self.set ^= bit

        # get move value for each piece that can move
        if self.capture_type == self.capture_forward:
            move_value = bit | (bit << self.shift)
            bit <<= 2 * self.shift
            # get eaten pieces for each move
            while (self.board.oppPieces.val & bit).val:
                move_value |= bit
                bit <<= self.shift
            return move_value
        elif self.capture_type == MoveGenerator.capture_backward:
            move_value = bit | (bit << self.shift)
            bit = rshift(bit, self.shift)
            while (self.board.oppPieces.val & bit).val:
                move_value |= bit
                bit = rshift(bit, self.shift)
            return move_value
        elif self.capture_type == MoveGenerator.no_capture:
            return bit | (bit << self.shift)
        elif self.capture_type == MoveGenerator.pass_move:
            return Piece(0)
        else:
            return Piece(-1)

    @staticmethod
    def arbitraryMove(board):
        # from board.Board import Boardmove
        i = MoveGenerator.arbitraryMoveIndex
        MoveGenerator.arbitraryMoveIndex += 1
        moveGenerator = MoveGenerator(board)
        while moveGenerator.hasMoreElements():
            move = moveGenerator.nextSet()
            i -= 1
            if i < 0:
                new_move = Board.from_move(board, move)
                return new_move
        MoveGenerator.arbitraryMoveIndex = 1
        newmg = MoveGenerator(board)
        move = newmg.nextSet()
        new_move = Board.from_move(board, move)
        return new_move


if __name__ == '__main__':
    # board = ["none", "one", "none", "none", "none", "one", "none", "none",
    #          "one", "none", "none", "one", "one", "none",
    #          "one", "one", "one", "none", "none", "none", "one", "none", "two",
    #          "none", "none", "one", "none", "two",
    #          "none", "two", "none", "two", "two", "two", "none", "two", "two",
    #          "two", "two", "two", "none", "two",
    #          "two", "two", "none", "two", "two", "two", "two", "two"]
    # my_pieces, opp_pieces = board_to_bit(board)
    # print(my_pieces, opp_pieces)
    # # hh = SetBoard(4611686018596683196, 9223927819925454848)
    # b = Board.from_ints(my_pieces, opp_pieces)
    # b.alpha_beta(0, -2147483647, 21474836470, 0)
    # # print(hh.best_move, hh.evaluation)

    # my = sum([1 << i for i in [25, 27, 35, 45, 62]])
    # opp = sum([1 << i for i in [22, 31, 24, 32, 2]])

    # my = 4611686018584018175
    # opp = -9222809671744618496

    # my = -4611686018404909825
    # opp = -9223020984202690560
    #
    # my = Player(my)
    # opp = Player(opp)

    # 4611686018449735103 -9223021190596001792
    # my = Player(-9222809671778172928)
    # opp = Player(-4611686018404975361)
    my = Player(-9223021190596001792)
    opp = Player(-4611686018405040705)
    b = Board(my, opp)
    b1 = Board.from_move(b, Piece(0))

    print(Evaluation.evaluate(b1, -37, -261, -211))
    # mv = MoveGenerator(b1)
    # print(mv.nextSet().val)
    # print(b)-9 217 267
    # (self, depth, alpha, beta, sequence_number)
    # b1.alpha_beta(-8, -2147483647, -236, 0)

    # print(b1.best_move.val, b1.evaluation)
