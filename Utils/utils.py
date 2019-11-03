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


def PiecesOnBoard(pieces, pieces2):
    """Returns pieces array, need optimization"""
    stones = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
    for i in range(5):
        for j in range(9):
            if (pieces & Bits.at(i, j)) != 0:
                stones[i][j] = '1'
            elif (pieces2 & Bits.at(i, j)) != 0:
                stones[i][j] = '2'
            else:
                stones[i][j] = '.'
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
    """Showing pieces on the board"""
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
