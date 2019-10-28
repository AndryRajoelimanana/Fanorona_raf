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
        stones = 0
        for i in range(5):
            for j in range(9):
                if (pieces & Bits.at(i, j)) != 0:
                    stones += 1
        return stones

    @staticmethod
    def lastBit(bitboard):
        return bitboard & -bitboard

