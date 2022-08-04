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
            print('%r  %2.6f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


class Bits:
    is_white = 4611686018427387904
    captured = 9223372036854775808
    initial_bot = 173538815
    initial_top = 562399469895680
    top_row = 561850441793536
    bottom_row = 511
    left_col = 281750123315456
    right_col = 1100586419201
    diagonal = 375116358920533
    on_board = 562399660211711
    center = 130023424
    shift_vertical = 10
    shift_horizontal = 1
    shift_slant = 11
    shift_backslant = 9

    @staticmethod
    def at(row, col):
        return 1 << (10 * (4 - row)) + (8 - col)

    @staticmethod
    def count(pieces):
        return bin(pieces & Bits.on_board).count('1')

    @staticmethod
    def last_bit(bitboard):
        return bitboard & -bitboard


def tobin(my):
    return "{0:064b}".format(my)



def get_board(my, opp):
    my = "{0:064b}".format(my)[-50:]
    opp = "{0:064b}".format(opp)[-50:]
    hh = []

    for i, j in zip(my, opp):
        if i == '1':
            if j == '1':
                raise
            hh.append('1')
        elif i == '0' and j == '1':
            hh.append('2')
        else:
            hh.append('.')
    print()
    for i in range(5):
        print(' ', '  '.join(hh[(i * 10)+1:((i + 1) * 10)]))
    # return hh


if __name__ == '__main__':
    my, op = 4611686018596683196, 9223927819925454848
    get_board(my, op)
