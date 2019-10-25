from Utils.Bits import Bits


def PiecesOnBoard(pieces, pieces2):
    '''Returns pieces array'''
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
    '''Showing pieces on the Board'''
    boardpieces = PiecesOnBoard(pieces, pieces2)
    ff = '\nmyPieces : %s \noppPieces : %s \n \n' % (pieces, pieces2)
    for i in range(5): ff = ff + '  ' + '  '.join(boardpieces[i][:]) + '\n'
    return ff


def getMoves(attackers, open_on_board, movetype):
    '''Returns moves for a specific move type'''
    return (attackers & rshift(open_on_board, movetype)) | (open_on_board & rshift(attackers, movetype))


def NegBit(val):
    '''Returs Negative Bit'''
    if (val | (1 << 63)) > (1 << 63):
        val = val - (1 << 63)
    return val


def PosBit(val):
    '''Returs Positive Bit'''
    if (val & (~(1 << 63))) < -(1 << 63):
        val = val + (1 << 63)
    return val


def rshift(val, n):
    return (val & 0xffffffffffffffff) >> n
