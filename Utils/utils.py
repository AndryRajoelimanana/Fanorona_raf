from Utils.Bits import Bits
from Utils.configs import *
from typing import TypeVar

PieceT = TypeVar('PieceT', bound='Piece')
PlayerT = TypeVar('PlayerT', bound='Player')
maxsize = (1 << 31) - 1


class Piece:
    def __init__(self, value=0):
        self.val = value

    @property
    def str(self):
        return "{0:064b}".format((self.val & Bits.on_board) % (1 << 64))

    @property
    def count(self):
        return self.str[14:].count('1')

    def index(self):
        bin_str = self.str[14:]
        return 0 if bin_str.count('1') != 1 else 49 - bin_str.index('1')

    def all_one(self):
        bin_str = self.str[14:]
        ones = []
        while True:
            try:
                ind = bin_str.index('1')
                ones.append(len(bin_str) - ind)
                bin_str = bin_str[ind+1:]
            except ValueError:
                break
        return ones

    def to_pos(self, numerics = False):
        pos_dict = {0: 'i', 1: 'h', 2: 'g', 3: 'f', 4: 'e', 5: 'd', 6: 'c',
                    7: 'b', 8: 'a'}
        ind = self.index()
        if numerics:
            return ind
        else:
            return f'{pos_dict[ind % 10]}{1 + (ind // 10)}'

    def __rshift__(self, other):
        other = self.check_input(other)
        if self.val < 0:
            return Piece((self.val % (2 ** 64)) >> other)
        else:
            return Piece(self.val >> other)

    @staticmethod
    def check_input(other: (PieceT, int)) -> int:
        return other.val if isinstance(other, Piece) else other

    def __invert__(self) -> PieceT:
        return Piece(~self.val)

    def __neg__(self) -> PieceT:
        return Piece(-self.val)

    def __and__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val & other)

    def __or__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val | other)

    def __xor__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val ^ other)

    def __rxor__(self, other) -> PieceT:
        other = self.check_input(other)
        return self.__xor__(other)

    def __lshift__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val << other)

    def __add__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val + other)

    def __sub__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val - other)

    def __ge__(self, other):
        other = self.check_input(other)
        return self.val >= other

    def __le__(self, other):
        other = self.check_input(other)
        return self.val <= other

    def __gt__(self, other):
        other = self.check_input(other)
        return self.val > other

    def __lt__(self, other):
        other = self.check_input(other)
        return self.val < other

    def __eq__(self, other):
        other = self.check_input(other)
        return self.val == other

    def __mod__(self, other) -> PieceT:
        other = self.check_input(other)
        return Piece(self.val % other)

    def __iadd__(self, other) -> PieceT:
        other = self.check_input(other)
        self.val += other
        return self

    def __ior__(self, other) -> PieceT:
        other = self.check_input(other)
        self.val |= other
        return self

    def __iand__(self, other) -> PieceT:
        other = self.check_input(other)
        self.val &= other
        return self

    def __ixor__(self, other) -> PieceT:
        other = self.check_input(other)
        self.val ^= other
        return self

    def __rrshift__(self, other) -> PieceT:
        return self.__rshift__(other)

    def __rand__(self, other) -> PieceT:
        return self.__and__(other)

    def __ror__(self, other) -> PieceT:
        return self.__or__(other)

    def __rlshift__(self, other) -> PieceT:
        return self.__lshift__(other)

    def __radd__(self, other) -> PieceT:
        return self.__add__(other)

    def __rsub__(self, other) -> PieceT:
        return self.__sub__(-other)

    @property
    def not_active_square(self) -> PieceT:
        return self & (~active_squares)

    @property
    def active_square(self) -> PieceT:
        return self & active_squares

    def __repr__(self):
        # if not self.val:
        #    return str(0)
        bb = to64(self.val)[14:]
        ff = ''
        for i in range(5):
            ff += '  '.join(
                bb[i * 10 + 1:(i + 1) * 10].replace('0', '.')) + '\n'
        return ff


class Player(Piece):
    def __init__(self, value):
        if value < 0:
            value = (1 << 64) + value
        super(Player, self).__init__(value & Bits.on_board)
        self.is_white = (value & Bits.is_white) != 0
        self.captured = (value & Bits.captured) != 0

    @property
    def str(self):
        return "{0:064b}".format(self.value % (1 << 64))
    # @property
    # def is_white(self):
    #     return self._is_white
    #
    # @property
    # def captured(self):
    #     return self._captured

    def list(self):
        return [list(self[i * 10 + 1:(i + 1) * 10]) for i in range(5)]

    def show_board(self):
        llist = self.list()
        print()
        for i in range(5):
            print("   ", "  ".join(llist[i]))

    def control(self, side='left'):
        if side == 'left':
            return rshift((self.val & left_control) - 1, 57)
        elif side == 'right':
            return rshift((self.val & right_control) - 1, 57)
        elif side == 'center':
            return rshift((self.val & center_control) - 1, 57)
        else:
            raise f'Pieces control side value {side} not valid'

    def activity(self, safe_moves: PieceT) -> PieceT:
        """
        Compute Pieces that can perform a safe move into an active square
        """

        nn = next_to(safe_moves) & active_squares
        act = nn | next_to(safe_moves.active_square)
        ff = (act | (active_squares & next_to(act & self))) & self
        return ff
        # if isinstance(ff.val, Piece) or isinstance(ff.val, Player):
        #     return ff
        # else:
        #     return Piece(ff)

    def attack(self, other) -> PieceT:
        open_board = self.open_board(other)
        unsafe = Piece(0)
        for i in [10, 1]:
            moves = get_moves(self.val, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        for i in [11, 9]:
            moves = get_moves(self.val & Bits.diagonal, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        return unsafe

    def open_board(self, other):
        return ~ (self.val | other.val)

    def captured_pieces(self, other) -> PieceT:
        my_attack = self.attack(other)
        return my_attack & other.val

    def can_capture(self, other):
        return self.captured_pieces(other)

    def fortress(self, type_='lg_left') -> PieceT:
        return self & dict_fortress[type_]

    def guard(self, type_='lg_left') -> PieceT:
        return self & dict_guard[type_]

    def to_attack(self, type_='lg_left') -> PieceT:
        return self & dict_attack[type_]

    @property
    def repr(self):
        is_white = int(self.is_white) << 62
        vv = self.val + is_white
        return vv - Bits.captured if self.captured else vv

    @property
    def value(self):
        is_white = int(self.is_white) << 62
        captured = int(self.captured) << 63
        return self.val + is_white + captured

    def __and__(self, other):
        parent_ = (int(self.captured) << 63) + (int(self.is_white) << 62)
        return Player(Piece.__and__(self, other).val + parent_)

    def __or__(self, other):
        parent_ = (int(self.captured) << 63) + (int(self.is_white) << 62)
        return Player(Piece.__or__(self, other).val + parent_)

    def __xor__(self, other):
        parent_ = (int(self.captured) << 63) + (int(self.is_white) << 62)
        return Player(Piece.__xor__(self, other).val + parent_)

    def __invert__(self):
        parent_ = (int(self.captured) << 63) + (int(self.is_white) << 62)
        return Player(Piece.__invert__(self).val + parent_)


def rshift(val, n):
    return (val & 0xffffffffffffffff) >> n


def format_eval(n):
    return f'{n // 100}.{n % 100:02}'


def to64(val):
    return format(val, '064b')


def eaten_pieces(moves: PieceT, movetype):
    return (moves >> movetype) | (moves << (2 * movetype))


def p_move(move: PieceT, type_=10) -> PieceT:
    return (move << type_) | (move >> type_)


def get_moves(attackers, open_board, movetype):
    """Returns moves for a specific move type"""
    return (attackers & (open_board >> movetype).val) | (
            open_board & (attackers >> movetype).val)


def unsafe_pieces(attackers, open_board, move_type):
    moves = get_moves(attackers, open_board, move_type)
    return eaten_pieces(moves, move_type)


def next_to(s: PieceT) -> PieceT:
    n = p_move(s, Bits.shift_vertical)
    s1 = s | (n & ~Bits.diagonal)
    return n | p_move(s1, Bits.shift_horizontal)


def evaluate_pieces(my_count, opp_count, control=0):
    if my_count == 0:
        return -(opp_count * won_position - 4 * ply_decrement)
    elif opp_count == 0:
        return my_count * won_position - ply_decrement
    if my_count >= opp_count:
        return control + (my_count - opp_count) * (ratios_eval[opp_count] +
                                                   piece_value * (control == 0))
    else:
        return control - (opp_count - my_count) * (ratios_eval[my_count] +
                                                   piece_value * (control == 0))


class Hash:
    collect_statistic_hash = True
    hits = 0
    misses = 0
    shallow = 0
    badBound = 0
    movedict = {}

    def __init__(self):
        pass

    @staticmethod
    def to_int(n):
        return n & ((1 << 32) - 1)

    @staticmethod
    def get_hash(board, hash_value, alpha, beta, depth):
        if hash_value in Hash.movedict:
            stored_value = Hash.movedict[hash_value]
            board.best_move = Piece(stored_value[0])
            board.forced = stored_value[1]
            evalType = stored_value[2]
            evalDepth = stored_value[3] - depth_adjustment
            evaluation = stored_value[4]

            if debug:
                print(f'get_hash {board.best_move.val} {evalType} {evalDepth} '
                      f'{evaluation}')
            if evalDepth < depth:
                if Hash.collect_statistic_hash:
                    Hash.shallow += 1
            elif evalType == board.eval_exact or (
                    (evalType == board.eval_upper_bound) and
                    (evaluation <= alpha)) or (
                    (evalType == board.eval_lower_bound) and
                    (evaluation >= beta)):
                board.evaluation = evaluation
                if Hash.collect_statistic_hash:
                    Hash.hits += 1
                if board.best_move >= 0 and (board.evaluation >= alpha) and (
                        board.evaluation <= beta):
                    board.set_child(board.best_move)
                    board.child.hasPVar = False
                    board.set_principal_variation()
                    if debug:
                        print("Tato hash")
                if debug:
                    print("in database")
                return True
            elif Hash.collect_statistic_hash:
                Hash.badBound += 1
        elif Hash.collect_statistic_hash:
            Hash.misses += 1
        return False

    @staticmethod
    def set_hash(board, evalType, depth):
        hash_value = hash(board)
        depth += depth_adjustment
        if depth < 0:
            return
        best_move = board.best_move.val
        forced = board.forced
        Hash.movedict[hash_value] = (best_move, forced, evalType, depth,
                                     board.evaluation)

    @staticmethod
    def total_hash():
        return Hash.hits + Hash.shallow + Hash.misses + Hash.badBound


def board_to_bit(board):
    my_pieces = 0
    opp_pieces = 0
    for i in range(50):
        if i != 0:
            if board[i] == 'one':
                opp_pieces = opp_pieces + (1 << i - 1)
            elif board[i] == 'two':
                my_pieces = my_pieces + (1 << i - 1)
    return my_pieces, opp_pieces


def pmv(nn):
    bb = to64(nn)[14:]
    ff = ''
    for i in range(5):
        ff += '  '.join(
            bb[i * 10 + 1:(i + 1) * 10].replace('0', '.')) + '\n'
    return ff


def PiecesOnBoard(pieces, pieces2, p1='1', p2='2', p0='.'):
    """Returns pieces array, need optimization"""
    stones = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
    for i in range(5):
        for j in range(9):
            if (pieces & Bits.at(i, j)) != 0:
                stones[i][j] = p1
            elif (pieces2 & Bits.at(i, j)) != 0:
                stones[i][j] = p2
            else:
                stones[i][j] = p0
    return stones


def pb(my, opp):
    bb = to64(my if my > 0 else (my + (1 << 63)))[14:]
    bb1 = to64(opp if opp > 0 else (opp + (1 << 63)))[14:]
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
    print(ff)


if __name__ == '__main__':
    n = Piece(33587232)
    print(n.all_one())
