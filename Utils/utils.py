from Utils.Bits import Bits
import re
from typing import TypeVar
import time

PiecesT = TypeVar('PiecesT', bound='Pieces')


list_moves = [10, 1, 11, 9]
active_squares = 92632243238996
# terms for broken-fortress evaluation
attack_weight = 600  # value of a successful attack
trapped_piece_weight = 100  # value of a trapped piece
conversion_weight = 35  # bonus for converting to simpler pos
max_positional_eval = 50  # expected max of next two terms
forward_weight = 10  # value of a piece in the attacking zone
space_weight = 1  # penalty for allowing defense liebensraum

# terms for eval of relatively even positions
piece_weight = 300  # multiplier for material ratio
piece_value = 100  # add this number to ratio of activeposn
attack_bonus = 50  # one side attacking but cant break fort

# extra depths to search if a capture is available on this or the next ply
capture_depth = -30
threat_depth = -15

left_control = 171865964544
right_control = 10741622784
center_control = 42966491136

# stuff for finding fortresses
sm_left_fort = 281887696617728
sm_left_guard = 206225735680
sm_left_attack = 105553149821024
lg_left_fort = 493097109127616
lg_left_guard = 51657097216
lg_left_attack = 26388287455256
sm_right_fort = 1102736002049
sm_right_guard = 2151680000
sm_right_attack = 13194143727628
lg_right_fort = 7712703265799
lg_right_guard = 25799188480
lg_right_attack = 52776591687728

dict_fortress = {'sm_left': 281887696617728,
                 'lg_left': 493097109127616,
                 'sm_right': 1102736002049,
                 'lg_right': 7712703265799}

dict_guard = {'sm_left': 206225735680,
              'lg_left': 51657097216,
              'sm_right': 2151680000,
              'lg_right': 25799188480}

dict_attack = {'sm_left': 105553149821024,
               'lg_left': 26388287455256,
               'sm_right': 13194143727628,
               'lg_right': 52776591687728}


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.6f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def bit_to_pieces(board):
    new_board = ['none'] * 50
    for i in range(49):
        bits_at_i = (1 << i)
        if board.myPieces & bits_at_i:
            new_board[i + 1] = 'two'
        elif board.opponentPieces & bits_at_i:
            new_board[i + 1] = 'one'
    return new_board


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


class Pieces:
    def __init__(self, value: int, ):
        self.val = value

    def __rshift__(self, other) -> PiecesT:
        if isinstance(other, int):
            if self.val < 0:
                return Pieces((self.val % (2 ** 64)) >> other)
            else:
                return Pieces(self.val >> other)
        elif isinstance(other, Pieces):
            if self.val < 0:
                return Pieces((self.val % (2 ** 64)) >> other)
            else:
                return Pieces(self.val >> other)

    def __invert__(self) -> PiecesT:
        return Pieces(~self.val)

    def __and__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val & other)
        elif isinstance(other, Pieces):
            return Pieces(self.val & other.val)

    def __or__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val | other)
        elif isinstance(other, Pieces):
            return Pieces(self.val | other.val)

    def __xor__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val ^ other)
        elif isinstance(other, Pieces):
            return Pieces(self.val ^ other.val)

    def __rxor__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val ^ other)
        elif isinstance(other, Pieces):
            return Pieces(self.val ^ other.val)

    def __lshift__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val << other)
        elif isinstance(other, Pieces):
            return Pieces(self.val << other.val)

    def __add__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val + other)
        elif isinstance(other, Pieces):
            return Pieces(self.val + other.val)

    def __sub__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val - other)
        elif isinstance(other, Pieces):
            return Pieces(self.val - other.val)

    def __rrshift__(self, other) -> PiecesT:
        if isinstance(other, int):
            if self.val < 0:
                return Pieces((self.val % (2 ** 64)) >> other)
            else:
                return Pieces(self.val >> other)
        elif isinstance(other, Pieces):
            if self.val < 0:
                return Pieces((self.val % (2 ** 64)) >> other)
            else:
                return Pieces(self.val >> other)

    def __rand__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val & other)
        elif isinstance(other, Pieces):
            return Pieces(self.val & other.val)

    def __ror__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val | other)
        elif isinstance(other, Pieces):
            return Pieces(self.val | other.val)

    def __rlshift__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val << other)
        elif isinstance(other, Pieces):
            return Pieces(self.val << other.val)

    def __radd__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val + other)
        elif isinstance(other, Pieces):
            return Pieces(self.val + other.val)

    def __rsub__(self, other) -> PiecesT:
        if isinstance(other, int):
            return Pieces(self.val - other)
        elif isinstance(other, Pieces):
            return Pieces(self.val - other.val)

    def __repr__(self):
        bb = to64(self.val)[14:]
        ff = ''
        for i in range(5):
            ff += '  '.join(bb[i*10+1:(i+1)*10].replace('0', '.')) + '\n'
        return ff

    @property
    def count(self):
        return self.on_board().str.count('1')

    @property
    def str(self):
        return "{0:064b}".format(self.val % (2 ** 64))

    def on_board(self) -> PiecesT:
        return Pieces(self.val & Bits.on_board)

    def list(self):
        return [list(self.on_board[i*10+1:(i+1)*10]) for i in range(5)]

    def show_board(self):
        llist = self.list()
        print()
        for i in range(5):
            print("   ", "  ".join(llist[i]))

    def control(self, side='left'):
        if side == 'left':
            return ((self & left_control) - 1) >> 57
        elif side == 'right':
            return ((self & right_control) - 1) >> 57
        elif side == 'center':
            return ((self & center_control) - 1) >> 57
        else:
            raise f'Pieces control side value {side} not valid'

    @property
    def next_to(self) -> PiecesT:
        """
        Compute positions that are adjacent to a particular pieces
        """
        s = self
        n = p_move(s, Bits.shift_vertical)
        s |= (n & ~Bits.diagonal)
        return n | p_move(s, Bits.shift_horizontal)

    def activity(self, safe_moves: PiecesT) -> PiecesT:
        """
        Compute Pieces that can perform a safe move into an active square
        """
        nn = (safe_moves.next_to() & active_squares)
        act = nn | safe_moves.not_active_square
        return Pieces((act | (active_squares & self.next_to(act & self))) &
                      self)

    def attack(self, open_board: PiecesT) -> PiecesT:
        unsafe = Pieces(0)
        for i in [10, 1]:
            moves = get_moves(self, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        for i in [11, 9]:
            moves = get_moves(self & Bits.diagonal, open_board, i)
            unsafe |= eaten_pieces(moves, i)
        return unsafe

    def fortress(self, type_='lg_left') -> PiecesT:
        return self & dict_fortress[type_]

    def guard(self, type_='lg_left') -> PiecesT:
        return self & dict_guard[type_]

    def to_attack(self, type_='lg_left') -> PiecesT:
        return self & dict_attack[type_]

    @property
    def not_active_square(self) -> PiecesT:
        return self & ~active_squares

    @property
    def active_square(self) -> PiecesT:
        return self & active_squares




# @timeit
# def PiecesOnBoard1(pieces, pieces2):
#     """Returns pieces array"""
#     stones = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
#     for matchtuple in re.finditer('1', format(pieces, '064b')):
#         match = 64 - matchtuple.start()
#         if ()
#         stones[row][col] = '2'
#     for matchtuple in re.finditer('1', format(pieces2,'064b')):
#         match = 64 - matchtuple.start()
#         row = (match // 10)
#         col = (match % 10) - 1
#         stones[row][col] = '1'
#     return stones


def ShowBoard(pieces, pieces2):
    """Showing pieces on the boardin"""
    board_pieces = PiecesOnBoard(pieces, pieces2)
    ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (pieces, pieces2)
    for i in range(5):
        ff = f'{ff}  ' + '  '.join(board_pieces[i][:]) + '\n'
    return ff


def open_on_board(board):
    occupied = board.myPieces | board.opponentPieces
    open_position = Bits.on_board & ~occupied
    return open_position


def eaten_pieces(moves, movetype):
    return rshift(moves, movetype) | (moves << (2 * movetype))

def p_move(move, type_=10):
    return (move << type_) | (move >> type_)

def get_moves(attackers, open_board, movetype):
    """Returns moves for a specific move type"""
    return (attackers & rshift(open_board, movetype)) | (open_board & rshift(attackers, movetype))


def unsafe_pieces(attackers, open_board, move_type):
    moves = get_moves(attackers, open_board, move_type)
    return eaten_pieces(moves, move_type)


def NegBit(val):
    """Returns Negative Bit"""
    if (val | (1 << 63)) > (1 << 63):
        val = val - (1 << 63)
    return val


def PosBit(val):
    """Returns Positive Bit"""
    if (val & (~(1 << 63))) < -(1 << 63):
        val = val + (1 << 63)
    return val


def get_bit(piece):
    bit_value = 0
    row = {'1': 0, '2': 10, '3': 20, '4': 30, '5': 40}
    column = {'a': 8, 'b': 7, 'c': 6, 'd': 5, 'e': 4, 'f': 3, 'g': 2, 'h': 1, 'i': 0}
    for j in piece:
        try:
            bit_value += 2 ** (column[j[0]] + row[j[1]])
        except KeyError:
            return 0
    return bit_value


def rshift(val, n):
    return (val & 0xffffffffffffffff) >> n


def pmv(nn):
    print(ShowBoard(nn, 0))


def pbrd(nn, nn1):
    print(ShowBoard(nn, nn1))


def two_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val


def to64(val):
    return format(val, '064b')


def neg(val):
    if val >= 0:
        val = val - (1 << 64)
    return val


def pos(val):
    return (1 << 63) - val


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


def get_hash(Board, board, hash_value, alpha, beta, depth):
    # print('Already in move dict')
    if hash_value in Board.movedict.keys():
        stored_value = Board.movedict[hash_value]
        board.best_move = stored_value[2]
        stored_eval_type = stored_value[3]
        board.forced = stored_value[4]
        stored_eval = stored_value[5]
        stored_depth = stored_value[6]
        if stored_depth >= depth:
            if stored_eval_type == Board.eval_exact or (
                    stored_eval_type == Board.eval_upper_bound and stored_eval <= alpha) or (
                    stored_eval_type == Board.eval_lower_bound and stored_eval >= beta):
                board.evaluation = stored_eval
                return True
    return False


def get_movelog(my_pieces, opp_pieces, move):
    mvlist = []
    initial_mv = findPiece(my_pieces & move)[0]
    mvlist.append(initial_mv)
    mvdict = dict()
    mvdict[str(initial_mv)] = [0]
    for mv in move_log:
        if mv > 0:
            openb = findPiece(~(my_pieces | opp_pieces | (1 << (mvlist[-1])-1)) & mv)[0]
            mvlist.append(openb)
            mvdict[str(openb)] = findPiece(opp_pieces & mv)
    return mvdict, mvlist


def findPiece(vv):
    nn = to64(vv)
    m = nn.rfind('1')
    nnn = []
    while m > 0:
        nnn.append(64 - m)
        m = nn.rfind('1', 0, m)
    return nnn
