from Bits import Bits
from Utils.utils import *


class Evaluation():

    active_squares = 92632243238996
    # terms for broken-fortress evaluation
    attack_weight = 600         # value of a successful attack
    trapped_piece_weight = 100  # value of a trapped piece
    conversion_weight = 35      # bonus for converting to simpler pos
    max_positional_eval = 50    # expected max of next two terms
    forward_weight = 10         # value of a piece in the attacking zone
    space_weight = 1            # penalty for allowing defense liebensraum

    # terms for eval of relatively even positions
    piece_weight = 300          # multiplier for material ratio
    piece_value = 100           # add this number to ratio of activeposn
    attack_bonus = 50           # one side attacking but cant break fort

    # extra depths to search if a capture is available on this or the next ply
    capture_depth = -30
    threat_depth = -15

    # bit masks for finding batteries
    left_margin = 211346952257728    # must be clear for battery
    left_battery = 262400            # must be set in battery test
    right_margin = 6612108457990     # must be clear for battery
    right_battery = 1025             # must be set in battery test

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
    # Which parts of the board have the strong squares controlled by one player?
    diagonal = 375116358920533
    left_control = 171865964544
    right_control = 10741622784
    center_control = 42966491136
    ratios = [2147483647]+[int(piece_weight/(i+1)) for i in range(64)]

    @staticmethod
    def attack(attackers, open_on_board):
        moves = getMoves(attackers, open_on_board, Bits.shift_vertical)


        moves = (rshift(attackers, Bits.shift_vertical) & openb)| (rshift(openb, Bits.shift_vertical) & attackers)
        unsafe = rshift(moves, Bits.shift_vertical) | (moves << (2 * Bits.shift_vertical))
        moves = (rshift(attackers, Bits.shift_horizontal) & openb) | (rshift(openb, Bits.shift_horizontal) & attackers)
        unsafe |= rshift(moves, Bits.shift_horizontal) | (moves << (2 * Bits.shift_horizontal))
        attackers &= Bits.diagonal
        moves = (rshift(attackers, Bits.shift_slant) & openb)| (rshift(openb, Bits.shift_slant) & attackers)
        unsafe |= rshift(moves, Bits.shift_slant) | (moves << (2 * Bits.shift_slant))
        moves = (rshift(attackers, Bits.shift_backslant) & openb)| (rshift(openb, Bits.shift_backslant) & attackers)
        return unsafe | (rshift(moves, Bits.shift_backslant) | (moves << (2 * Bits.shift_backslant)))

    @staticmethod
    def nextTo(s):
        n = (rshift(s, Bits.shift_vertical)) | (s << Bits.shift_vertical)
        s |= (n &  ~Bits.diagonal)
        return n | (rshift(s, Bits.shift_horizontal)) | (s << Bits.shift_horizontal)

    @staticmethod
    def activity(pieces, safeMoves):
        act = (Evaluation.active_squares & Evaluation.nextTo(safeMoves)) | Evaluation.nextTo(Evaluation.active_squares & safeMoves)
        return (act | (Evaluation.active_squares & Evaluation.nextTo(act & pieces))) & pieces

    @staticmethod
    def evaluate(b, alpha=-2147483648, beta=2147483647, depth=-2147483647):
        from Board import Board
        myPieces = b.myPieces & Bits.on_board
        opponentPieces = b.opponentPieces & Bits.on_board
        myPieceCount = Bits.count(myPieces)
        oppPieceCount = Bits.count(opponentPieces)
        if ((myPieceCount <= 2) and (oppPieceCount <=2)):
            return True

        open_position = open_on_board(b)
        myAttacks = Evaluation.attack(myPieces, open_position)
        if ((myAttacks & opponentPieces) !=0):
            oppPieceCount -= 1
            if (oppPieceCount == 0):
                b.evaluation = myPieceCount * Board.won_position - Board.ply_decrement
                return True
            if (depth > Evaluation.capture_depth):
                return False
            if (myPieceCount >= oppPieceCount):
                b.evaluation = (myPieceCount - oppPieceCount) * (Evaluation.ratios[oppPieceCount] + Evaluation.piece_value)
            else:
                b.evaluation = -(oppPieceCount - myPieceCount) * (Evaluation.ratios[myPieceCount] + Evaluation.piece_value)
            return True

        oppAttacks = Evaluation.attack(opponentPieces, open_position)
        mySafeMoves = open_position & ~oppAttacks
        myActive = Evaluation.activity(myPieces, mySafeMoves)
        attacked = myPieces & oppAttacks
        if ((myActive == 0) or ((attacked & myActive) != attacked) or ((attacked & (attacked -1)) != 0)):
            myPieceCount -= 1
            if (myPieceCount == 0):
                b.evaluation = -(oppPieceCount * Board.won_position - 4*Board.ply_decrement)
                return True
            if (depth > Evaluation.capture_depth):
                return False
        elif (attacked != 0):
            if (depth > Evaluation.threat_depth):
                return False

        control = int(rshift(((opponentPieces & Evaluation.left_control) - 1), 57))
        - int(rshift(((myPieces & Evaluation.left_control) - 1), 57))
        + int(rshift(((opponentPieces & Evaluation.center_control) - 1), 57))
        - int(rshift(((myPieces & Evaluation.center_control) - 1), 57))
        + int(rshift(((opponentPieces & Evaluation.right_control) - 1), 57))
        - int(rshift(((myPieces & Evaluation.right_control) - 1), 57))

        # Compute opponent active Pieces. Count active Pieces.
        oppSafeMoves = open_position & ~myAttacks
        oppActive = Evaluation.activity(opponentPieces, oppSafeMoves)
        myActivity = Bits.count(myActive)
        oppActivity = Bits.count(oppActive)

        if (myActivity == oppActivity):
            myPieceCount += myActivity
            oppPieceCount += oppActivity
            if (myPieceCount >= oppPieceCount):
                # print(myPieces, opponentPieces, myActivity, myPieceCount, oppActivity, oppPieceCount)
                b.evaluation = control + (myPieceCount - oppPieceCount) * Evaluation.ratios[oppPieceCount]
            else:
                b.evaluation = control - (oppPieceCount - myPieceCount) * Evaluation.ratios[myPieceCount]
            return True
        if (myActivity > oppActivity):
            attacking = True
            attackingPieces = myPieces
            attackingActivity = myActivity
            attackingTrapped = myPieceCount - myActivity
            defendingPieces = opponentPieces
            defendingActivity = oppActivity
            stuckDefenders = opponentPieces & ~oppActive
            defendingTrapped = oppPieceCount - oppActivity
            safeForDefense = oppSafeMoves
        else:
            attacking = False;
            attackingPieces = opponentPieces
            attackingActivity = oppActivity
            attackingTrapped = oppPieceCount - oppActivity
            defendingPieces = myPieces
            defendingActivity = myActivity
            stuckDefenders = myPieces & ~myActive
            defendingTrapped = myPieceCount - myActivity
            safeForDefense = mySafeMoves
            control = -control
            x = alpha
            alpha = -beta
            beta = -x
        if (((defendingActivity + defendingTrapped) == 1)
            and (attackingActivity >= 2) and (attackingTrapped == 0)
            and ((safeForDefense & Evaluation.nextTo(attackingPieces &
             ~Evaluation.active_squares)) == 0)
             and ((safeForDefense & Evaluation.nextTo(attackingPieces) &
              Evaluation.nextTo(defendingPieces)) == 0)):
            b.evaluation = int(attackingActivity * Board.won_position - (Board.won_position / 2) + control)
            if not (attacking):
                b.evaluation = -b.evaluation
            return True
        # Find fortresses and estimate material cost to break them
        attackZone = 0
        fortress = 0
        fortressStrength = 0
        if (((Evaluation.lg_left_fort & attackingPieces) == 0)
            and ((Evaluation.lg_left_guard & defendingPieces) != 0)):
            print('tato lg_left')
            fortress = Evaluation.lg_left_fort & defendingPieces
            fortress &= fortress - 1
            if (fortress != 0):
                fortress &= fortress - 1
                if (fortress == 0):
                    fortressStrength = 1
                else:
                    fortressStrength = 2
                attackZone = Evaluation.lg_left_attack;
                if ((Evaluation.lg_left_guard & stuckDefenders) != 0):
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif (((Evaluation.sm_left_fort & attackingPieces) == 0)
            and ((Evaluation.sm_left_guard & defendingPieces) != 0)):
            print('tato sm_left')
            fortress = Evaluation.sm_left_fort & defendingPieces
            fortress &= fortress - 1;
            if (fortress != 0):
                fortressStrength = 1
                attackZone = Evaluation.sm_left_attack
                if ((Evaluation.sm_left_guard & stuckDefenders) != 0):
                    defendingActivity += 1
                    defendingTrapped -= 1

        # large and small right fortresses
        if (((Evaluation.lg_right_fort & attackingPieces) == 0) and ((Evaluation.lg_right_guard & defendingPieces) != 0)):
            print('tato lg_right')
            fortress = Evaluation.lg_right_fort & defendingPieces
            fortress &= fortress - 1;
            if (fortress != 0):
                fortress &= fortress - 1;
                if (fortress == 0):
                    fortressStrength += 1
                else:
                    fortressStrength += 2
                attackZone |= Evaluation.lg_right_attack;
                if ((Evaluation.lg_right_guard & stuckDefenders) != 0):
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif (((Evaluation.sm_right_fort & attackingPieces) == 0)
            and ((Evaluation.sm_right_guard & defendingPieces) != 0)):
            print('tato sm_right')
            fortress = Evaluation.sm_right_fort & defendingPieces
            fortress &= fortress - 1
            if (fortress != 0):
                fortressStrength += 1
                attackZone |= Evaluation.sm_right_attack
                if ((Evaluation.sm_right_guard & stuckDefenders) != 0):
                    defendingActivity += 1
                    defendingTrapped -= 1

        if (fortressStrength == 0):
            fortressStrength = rshift(control, 31)

        if (attackingActivity - defendingActivity - fortressStrength > 0):
            evalb = Evaluation.attack_weight * (attackingActivity - defendingActivity-fortressStrength) + Evaluation.trapped_piece_weight *(attackingTrapped - defendingTrapped) - Evaluation.conversion_weight * defendingActivity
        else:
            a = 2 * attackingActivity + attackingTrapped
            d = 2 * defendingActivity + defendingTrapped
            if (a > d):
                evalb = (a - d) * Evaluation.ratios[d]
            elif (d > a):
                evalb = (d - a) * Evaluation.ratios[a]
            else:
                evalb = 0
            evalb += control + Evaluation.attack_bonus

        if ((evalb + Evaluation.max_positional_eval > alpha) and (evalb - Evaluation.max_positional_eval < beta)):
            space = defendingPieces
            while True:
                newSpace =  space | ((Evaluation.nextTo(space) & safeForDefense))
                if (space == newSpace):
                    break
                space =  newSpace

            evalb += Evaluation.forward_weight * Bits.count(attackingPieces & attackZone) - Evaluation.space_weight * Bits.count(space)

        if(attacking):
            b.evaluation = evalb
        else:
            b.evaluation = -evalb
        return True


