from Utils.Bits import Bits
import re
import time


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
        ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
    return ff


def open_on_board(board):
    occupied = board.myPieces | board.opponentPieces
    open_position = Bits.on_board & ~occupied
    return open_position


def eaten_pieces(moves, movetype):
    return rshift(moves, movetype) | (moves << (2 * movetype))


def get_moves(attackers, open_board, movetype):
    """Returns moves for a specific move type"""
    return (attackers & rshift(open_board, movetype)) | (open_board & rshift(attackers, movetype))


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
            print(openb)
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
