
# !/usr/bin/env python3


from Bits import Bits
from hashhh import Hash
import time
current_milli_time = lambda: int(round(time.time() * 1000))


class Board:
    pvs = True
    iid = True
    iid_ply = 25
    iid_limit = 55
    min_hash_depth = 15
    ply = 10
    forced_move_extension = 5
    forced_capture_extension = 10
    endgame_capture_extension = 5
    forced_endgame_capture = 10
    multiple_capture_extension = 7
    early_pass_extension = 10
    won_position = 10000
    decrementable = 5000
    ply_decrement = 1
    hash1 = Hash(32768)
    eval_upper_bound = 0
    eval_lower_bound = 1
    eval_exact = 2
    collect_extra_statistics = False
    sequenceNumber = 0
    leafCount = 0
    nodeCount = 0
    boardConsCount = 0
    moveGenConsCount = 0
    pvChangeCount = 0
    endgameDatabase = None
    maxsize = 2147483647

    def __init__(self, blackattop=True, whitegoesfirst=True):

        self.evaluation = None
        self.bestMove = -1
        self.principalVariation = None
        self.child = None
        self.moveGenerator = None
        self.forced = False
        self.hasPrincipalVariation = None
        self.table = {}
        self.reset(blackattop = True, whitegoesfirst=True)

    # Initial board
    def reset(self, blackattop = True, whitegoesfirst=True):
        self.previousPosition = None
        self.alreadyVisited = 0
        ImOnTop = (blackattop ^ whitegoesfirst)  # Who is on Top
        if ImOnTop:
            self.myPieces = Bits.initial_top
            self.opponentPieces = Bits.initial_bot
        else:
            self.myPieces = Bits.initial_bot
            self.opponentPieces = Bits.initial_top

        # Who goes first?
        if whitegoesfirst:
            self.myPieces = self.myPieces | Bits.is_white   # bottom and white
        else:
            self.opponentPieces = self.opponentPieces | Bits.is_white



    def twosComplement (value, bitLength=64) :
        return format(value & (2**bitLength - 1),'064b')

    def nn(self, nnn):
        g = twosComplement(nnn,64)
        h = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
        for i in range(5):
            h[i][:]=g[i*10+15:(i+1)*10+14]
        return h

    def __str__(self):
        ff = ''
        for i in range(5): ff = ff+'  '.join(bb[i][:])+'\n'
        return








