from Utils.Bits import Bits


def PiecesOnBoard(pieces, pieces2):
    """Returns pieces array"""
    stones = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
    for i in range(5):
        for j in range(9):
            if ((pieces & Bits.at(i, j)) != 0):
                stones[i][j] = '1'
            elif ((pieces2 & Bits.at(i, j)) != 0):
                stones[i][j] = '2'
            else:
                stones[i][j] = '.'
    return stones


def ShowBoard(pieces, pieces2):
    """Showing pieces on the Board"""
    board_pieces = PiecesOnBoard(pieces, pieces2)
    ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (pieces, pieces2)
    for i in range(5): ff = ff + '  ' + '  '.join(board_pieces[i][:]) + '\n'
    return ff


def open_on_board(board):
    occupied = board.myPieces | board.opponentPieces
    open_position = Bits.on_board & ~occupied
    return open_position


def eaten_pieces(moves, movetype):
    return rshift(moves, movetype) | (moves << (2 * movetype))


def getMoves(attackers, open_board, movetype):
    """Returns moves for a specific move type"""
    return (attackers & rshift(open_board, movetype)) | (open_board & rshift(attackers, movetype))


def NegBit(val):
    """Returs Negative Bit"""
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
