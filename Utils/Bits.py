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
    is_white = 1 << 62
    captured = 1 << 63
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
        return bin(pieces.val & Bits.on_board).count('1')

    @staticmethod
    def last_bit(bitboard):
        return bitboard & -bitboard


# from utils import rshift


# def vvv(x):
#     x -= rshift(x, 1) & 0x5555555555555555
#     x = (x & 0x3333333333333333) + (rshift(x, 2) & 0x3333333333333333)
#     res = x + rshift(x, 32)
#     return rshift(((res & 0x0f0f0f0f) + (rshift(res, 4) & 0x0f0f0f0f)) *
#                   0x01010101, 24)


