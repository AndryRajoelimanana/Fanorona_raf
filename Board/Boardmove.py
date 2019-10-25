from Board.Board import Board
class Boardmove(Board):
    def __init__(self, previousPosition, move):
        super().__init__()
        self.previousPosition = previousPosition
        captures = previousPosition.opponentPieces & move
        if (captures != 0):
            self.opponentPieces = utils.NegBit(previousPosition.opponentPieces ^ captures)
            move ^= captures
            self.alreadyVisited = previousPosition.alreadyVisited | move
            self.myPieces = utils.NegBit(previousPosition.myPieces ^ move)
        else:
            oppp = previousPosition.opponentPieces
            self.opponentPieces = previousPosition.myPieces ^ move
            self.myPieces = utils.PosBit(oppp)
            self.alreadyVisited = 0