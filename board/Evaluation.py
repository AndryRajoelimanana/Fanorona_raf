from Utils.Bits import Bits
from Utils.utils import *


class Evaluation:
    active_squares = 92632243238996
    # terms for broken-fortress evaluation
    attack_weight = 600  # value of a successful attack
    trapped_piece_weight = 100  # value of a trapped piece
    conversion_weight = 35  # bonus for converting to simpler pos
    max_positional_eval = 50  # expected max of next two terms
    forward_weight = 10  # value of a piece in the attacking zone
    space_weight = 1  # penalty for allowing defense liebensraum

    # terms for eval of relatively even positions
    piece_weight = 300  # multiplier for material ratio
    piece_value = 100  # add this number to ratio of activeposn
    attack_bonus = 50  # one side attacking but cant break fort

    # extra depths to search if a capture is available on this or the next ply
    capture_depth = -30
    threat_depth = -15

    # bit masks for finding batteries
    left_margin = 211346952257728  # must be clear for battery
    left_battery = 262400  # must be set in battery test
    right_margin = 6612108457990  # must be clear for battery
    right_battery = 1025  # must be set in battery test

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
    ratios = [2147483647] + [int(300 / (i + 1)) for i in range(64)]

    @staticmethod
    def attack(attackers, open_board):
        """
        Compute attacks by a player

        :param attackers: attacking piece
        :param open_board: open board (not my pieces, nor opponent pieces)
        :return: all positions that can be eaten by the attackers

        """

        shift_type = Bits.shift_vertical
        moves = get_moves(attackers, open_board, shift_type)
        unsafe_pieces = eaten_pieces(moves, shift_type)

        shift_type = Bits.shift_horizontal
        moves = get_moves(attackers, open_board, shift_type)
        unsafe_pieces |= eaten_pieces(moves, shift_type)

        attackers &= Bits.diagonal

        shift_type = Bits.shift_slant
        moves = get_moves(attackers, open_board, shift_type)
        unsafe_pieces |= eaten_pieces(moves, shift_type)

        shift_type = Bits.shift_backslant
        moves = get_moves(attackers, open_board, shift_type)
        unsafe_pieces |= eaten_pieces(moves, shift_type)

        return unsafe_pieces

    @staticmethod
    def next_to(s):
        """
        Compute positions that are adjacent to a particular pieces
        :param s:
        :return:
        """
        n = (rshift(s, Bits.shift_vertical)) | (s << Bits.shift_vertical)
        s |= (n & ~Bits.diagonal)
        return n | (rshift(s, Bits.shift_horizontal)) | (s << Bits.shift_horizontal)

    @staticmethod
    def activity(pieces, safe_moves):
        """
        Compute Pieces that can perform a safe move into an active square

        :param pieces:
            my pieces
        :param safe_moves:
            open position and not opponent attack
        :return:
            Pieces that can perform a safe move into an active square
        """
        act = (Evaluation.active_squares & Evaluation.next_to(safe_moves)) | Evaluation.next_to(
            Evaluation.active_squares & safe_moves)
        return (act | (Evaluation.active_squares & Evaluation.next_to(act & pieces))) & pieces

    def score_capture(self):
        # TODO
        pass

    @staticmethod
    def evaluate(b, alpha=-2147483648, beta=2147483648, depth=-2147483648):
        my_pieces = b.myPieces & Bits.on_board
        opponent_pieces = b.opponentPieces & Bits.on_board
        my_piece_count = Bits.count(my_pieces)
        opp_piece_count = Bits.count(opponent_pieces)

        if (my_piece_count <= 2) and (opp_piece_count <= 2):
            return True

        open_position = open_on_board(b)
        my_attacks = Evaluation.attack(my_pieces, open_position)
        # will next move is a capture return evaluate = True
        if (my_attacks & opponent_pieces) != 0:
            opp_piece_count -= 1
            if opp_piece_count == 0:  # will capture win?
                b.evaluation = my_piece_count * b.won_position - b.ply_decrement
                return True
            if depth > Evaluation.capture_depth:  # make a deeper search
                return False
            if my_piece_count >= opp_piece_count:
                b.evaluation = (my_piece_count - opp_piece_count) * (
                        Evaluation.ratios[opp_piece_count] + Evaluation.piece_value)
            else:
                b.evaluation = -(opp_piece_count - my_piece_count) * (
                        Evaluation.ratios[my_piece_count] + Evaluation.piece_value)
            return True

        # Run the following if my piece is not capturing
        opp_attacks = Evaluation.attack(opponent_pieces, open_position)
        my_safe_moves = open_position & ~opp_attacks

        # my_active = my active piece that can move safely
        my_active = Evaluation.activity(my_pieces, my_safe_moves)

        # attacked: my attacked piece
        attacked = my_pieces & opp_attacks

        # Check if:
        #   - any of my piece can't move safely (ever move to capture or to trapped position)
        #   - attacked pieces are already trap
        #   - too many capture to evade
        if (my_active == 0) or ((attacked & my_active) != attacked) or ((attacked & (attacked - 1)) != 0):
            my_piece_count -= 1
            if my_piece_count == 0:
                b.evaluation = -(opp_piece_count * b.won_position - 4 * b.ply_decrement)
                return True
            if depth > Evaluation.capture_depth:  # make a deeper search
                return False
        elif attacked != 0:
            if depth > Evaluation.threat_depth:
                return False

        # Who control the square if no piece in the control square it return 127 else 0
        control = rshift(((opponent_pieces & Evaluation.left_control) - 1), 57) - \
                  rshift(((my_pieces & Evaluation.left_control) - 1), 57) + \
                  rshift(((opponent_pieces & Evaluation.center_control) - 1), 57) - \
                  rshift(((my_pieces & Evaluation.center_control) - 1), 57) + \
                  rshift(((opponent_pieces & Evaluation.right_control) - 1), 57) - \
                  rshift(((my_pieces & Evaluation.right_control) - 1), 57)

        # Compute opponent active Pieces. Count active Pieces.
        oppSafeMoves = open_position & ~my_attacks
        opp_active = Evaluation.activity(opponent_pieces, oppSafeMoves)
        myActivity = Bits.count(my_active)
        oppActivity = Bits.count(opp_active)

        if myActivity == oppActivity:
            my_piece_count += myActivity
            opp_piece_count += oppActivity
            if my_piece_count >= opp_piece_count:
                b.evaluation = control + (my_piece_count - opp_piece_count) * Evaluation.ratios[opp_piece_count]
            else:
                b.evaluation = control - (opp_piece_count - my_piece_count) * Evaluation.ratios[my_piece_count]
            return True
        if myActivity > oppActivity:
            attacking = True
            attackingPieces = my_pieces
            attackingActivity = myActivity
            attackingTrapped = my_piece_count - myActivity
            defendingPieces = opponent_pieces
            defendingActivity = oppActivity
            stuckDefenders = opponent_pieces & ~opp_active
            defendingTrapped = opp_piece_count - oppActivity
            safeForDefense = oppSafeMoves
        else:
            attacking = False
            attackingPieces = opponent_pieces
            attackingActivity = oppActivity
            attackingTrapped = opp_piece_count - oppActivity
            defendingPieces = my_pieces
            defendingActivity = myActivity
            stuckDefenders = my_pieces & ~my_active
            defendingTrapped = my_piece_count - myActivity
            safeForDefense = my_safe_moves
            control = -control
            alpha, beta = -beta, -alpha

        if (((defendingActivity + defendingTrapped) == 1)
                and (attackingActivity >= 2) and (attackingTrapped == 0)
                and ((safeForDefense & Evaluation.next_to(attackingPieces &
                                                          ~Evaluation.active_squares)) == 0)
                and ((safeForDefense & Evaluation.next_to(attackingPieces) &
                      Evaluation.next_to(defendingPieces)) == 0)):
            b.evaluation = int(attackingActivity * b.won_position - (b.won_position / 2) + control)
            if not attacking:
                b.evaluation = -b.evaluation
            return True
        # Find fortresses and estimate material cost to break them
        attackZone = 0
        fortress = 0
        fortressStrength = 0
        if (((Evaluation.lg_left_fort & attackingPieces) == 0)
                and ((Evaluation.lg_left_guard & defendingPieces) != 0)):
            fortress = Evaluation.lg_left_fort & defendingPieces
            fortress &= fortress - 1
            if fortress != 0:
                fortress &= fortress - 1
                if fortress == 0:
                    fortressStrength = 1
                else:
                    fortressStrength = 2
                attackZone = Evaluation.lg_left_attack
                if (Evaluation.lg_left_guard & stuckDefenders) != 0:
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif (((Evaluation.sm_left_fort & attackingPieces) == 0)
              and ((Evaluation.sm_left_guard & defendingPieces) != 0)):
            fortress = Evaluation.sm_left_fort & defendingPieces
            fortress &= fortress - 1
            if fortress != 0:
                fortressStrength = 1
                attackZone = Evaluation.sm_left_attack
                if (Evaluation.sm_left_guard & stuckDefenders) != 0:
                    defendingActivity += 1
                    defendingTrapped -= 1

        # large and small right fortresses
        if (((Evaluation.lg_right_fort & attackingPieces) == 0) and (
                (Evaluation.lg_right_guard & defendingPieces) != 0)):
            fortress = Evaluation.lg_right_fort & defendingPieces
            fortress &= fortress - 1
            if fortress != 0:
                fortress &= fortress - 1
                if fortress == 0:
                    fortressStrength += 1
                else:
                    fortressStrength += 2
                attackZone |= Evaluation.lg_right_attack
                if (Evaluation.lg_right_guard & stuckDefenders) != 0:
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif (((Evaluation.sm_right_fort & attackingPieces) == 0)
              and ((Evaluation.sm_right_guard & defendingPieces) != 0)):
            fortress = Evaluation.sm_right_fort & defendingPieces
            fortress &= fortress - 1
            if fortress != 0:
                fortressStrength += 1
                attackZone |= Evaluation.sm_right_attack
                if (Evaluation.sm_right_guard & stuckDefenders) != 0:
                    defendingActivity += 1
                    defendingTrapped -= 1

        if fortressStrength == 0:
            fortressStrength = rshift(control, 31)

        if attackingActivity - defendingActivity - fortressStrength > 0:
            evalb = Evaluation.attack_weight * (
                    attackingActivity - defendingActivity - fortressStrength) + Evaluation.trapped_piece_weight * (
                            attackingTrapped - defendingTrapped) - Evaluation.conversion_weight * defendingActivity
        else:
            a = 2 * attackingActivity + attackingTrapped
            d = 2 * defendingActivity + defendingTrapped
            if a > d:
                evalb = (a - d) * Evaluation.ratios[d]
            elif d > a:
                evalb = (d - a) * Evaluation.ratios[a]
            else:
                evalb = 0
            evalb += control + Evaluation.attack_bonus

        if (evalb + Evaluation.max_positional_eval > alpha) and (evalb - Evaluation.max_positional_eval < beta):
            space = defendingPieces
            while True:
                newSpace = space | (Evaluation.next_to(space) & safeForDefense)
                if space == newSpace:
                    break
                space = newSpace

            evalb += Evaluation.forward_weight * Bits.count(
                attackingPieces & attackZone) - Evaluation.space_weight * Bits.count(space)

        if attacking:
            b.evaluation = evalb
        else:
            b.evaluation = -evalb
        return True
