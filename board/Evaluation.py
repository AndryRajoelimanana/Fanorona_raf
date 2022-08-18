import os
# printing environment variables
print(os.environ['PATH'])
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

    min_eval = - maxsize

    def score_capture(self):
        # TODO
        pass

    @staticmethod
    def evaluate(b, alpha=-2147483648, beta=2147483648,
                 depth=-2147483648):
        """
        Evaluation function itself
        Returns true with eval in b.evaluation, or false if depth is too high
        """
        my_pieces = b.myPieces
        opp_pieces = b.oppPieces
        my_piece_count = my_pieces.count
        opp_piece_count = opp_pieces.count
        evalb = None
        if (my_piece_count <= 2) and (opp_piece_count <= 2):
            return True

        # IF DEPTH is TOO HIGH return FALSE
        # open_position = b.open
        # my_attacks = my_pieces.attack(open_position)
        # will next move is a capture return evaluate = True
        if b.my_capture().val:
            opp_piece_count -= 1
            if opp_piece_count == 0:  # will capture win?
                evaluation = evaluate_pieces(my_piece_count, opp_piece_count)
                return evaluation
            if depth > Evaluation.capture_depth:  # make a deeper search
                return None
            evaluation = evaluate_pieces(my_piece_count, opp_piece_count)
            return evaluation

        # Run the following if my piece is not capturing
        my_active = b.my_activity()
        # attacked: my attacked piece
        attacked = b.opp_capture()

        # Check if:
        #   - any of my piece can't move safely (ever move into capture or to
        #   trapped position)
        #   - attacked pieces are already trap
        #   - too many capture to evade
        if (my_active == 0) or ((attacked & my_active) != attacked) or (
                (attacked & (attacked - 1)) != 0):
            my_piece_count -= 1
            if my_piece_count == 0:
                evaluation = evaluate_pieces(my_piece_count, opp_piece_count)
                return evaluation
            if depth > Evaluation.capture_depth:  # make a deeper search
                return None
        elif attacked != 0:
            if depth > Evaluation.threat_depth:
                return None

        # Who control the square if no piece in the control square it return
        # 127 else 0
        control = b.control()
        if debug:
            print(f'CONTROL : {control}')

        # Compute opponent active Pieces. Count active Pieces.
        # oppSafeMoves = open_position & ~my_attacks
        # opp_active = opp_pieces.activity(oppSafeMoves)
        myActivity = my_active.count
        oppActivity = b.opp_activity().count

        if myActivity == oppActivity:
            my_piece_count += myActivity
            opp_piece_count += oppActivity
            evaluation = evaluate_pieces(my_piece_count, opp_piece_count,
                                         control=control)
            if debug:
                print(
                    f'CONTROL : {evaluation} {my_piece_count} {opp_piece_count} {ratios[opp_piece_count]} {ratios[my_piece_count]}')
            return evaluation

        opponent_pieces = b.oppPieces
        opp_active = b.opp_activity()
        oppSafeMoves = b.opp_safemove()
        my_safe_moves = b.my_safemove()

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
                and (attackingActivity >= 2)
                and (attackingTrapped == 0)
                and not (safeForDefense & next_to(
                    attackingPieces.not_active_square))
                and not ((safeForDefense & next_to(attackingPieces)) &
                         next_to(defendingPieces))):
            evaluation = int(attackingActivity * b.won_position - (
                    b.won_position / 2) + control)
            if debug:
                print(f'CONTROL : {evaluation} {attackingActivity}')
            if not attacking:
                evaluation = -evaluation
            return evaluation
        # Find fortresses and estimate material cost to break them
        attackZone = 0
        # fortress = 0
        fortressStrength = 0
        defendingActivity = defendingActivity
        defendingTrapped = defendingTrapped

        if not attackingPieces.fortress() and defendingPieces.guard():
            fortress = defendingPieces.fortress('lg_left')
            # if piece in fortress greater than 1
            fortress = fortress & (fortress - 1)
            if fortress != 0:
                fortress = fortress & (fortress - 1)
                if fortress == 0:
                    fortressStrength = 1
                else:
                    fortressStrength = 2
                attackZone = lg_left_attack
                if stuckDefenders.guard('lg_left'):
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif not attackingPieces.fortress('sm_left') and \
                defendingPieces.guard('sm_left'):
            fortress = defendingPieces.fortress('sm_left')
            fortress = fortress & (fortress - 1)
            if fortress != 0:
                fortressStrength = 1
                attackZone = sm_left_attack
                if stuckDefenders.guard('sm_left'):
                    defendingActivity += 1
                    defendingTrapped -= 1

        # large and small right fortresses
        if not attackingPieces.fortress('lg_right') and \
                defendingPieces.guard('lg_right'):
            fortress = defendingPieces.fortress('lg_right')
            fortress = fortress & (fortress - 1)
            if fortress != 0:
                fortress = fortress & (fortress - 1)
                if fortress == 0:
                    fortressStrength += 1
                else:
                    fortressStrength += 2
                attackZone |= lg_right_attack
                if stuckDefenders.guard('lg_right'):
                    defendingActivity += 1
                    defendingTrapped -= 1

        elif not attackingPieces.fortress('sm_right') and \
                defendingPieces.guard('sm_right'):
            fortress = defendingPieces.fortress('sm_right')
            fortress = fortress & (fortress - 1)
            if fortress != 0:
                fortressStrength += 1
                attackZone |= sm_right_attack
                if stuckDefenders.guard('sm_right'):
                    defendingActivity += 1
                    defendingTrapped -= 1

        if fortressStrength == 0:
            fortressStrength = 1 if control < 0 else 0
        if attackingActivity - defendingActivity - fortressStrength > 0:
            evalb = Evaluation.attack_weight * (
                    attackingActivity - defendingActivity - fortressStrength) + Evaluation.trapped_piece_weight * (
                            attackingTrapped - defendingTrapped) - Evaluation.conversion_weight * defendingActivity
            if debug:
                print(f'Eval : Fortress broken{evalb} {attackingActivity}'
                      f' {defendingActivity} {fortressStrength}')
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

        if (evalb + Evaluation.max_positional_eval > alpha) and (
                evalb - Evaluation.max_positional_eval < beta):
            space = defendingPieces
            while True:
                newSpace = space | (next_to(space) & safeForDefense)
                if space == newSpace:
                    break
                space = newSpace

            evalb += Evaluation.forward_weight * (
                    attackingPieces & attackZone).count - Evaluation.space_weight \
                     * space.count
            if debug:
                print(f'Eval : slower low-order eval {space.val} {attackZone} '
                      f'{evalb}')

        evaluation = evalb if attacking else -evalb
        return evaluation

    # @staticmethod
    # def find_control(piece, side='left'):
    #     if side == 'left':
    #         return rshift(((piece & Evaluation.left_control) - 1), 57)


from Utils.board_utils import *

if __name__ == '__main__':
    # my = 4611686018596683192 & Bits.on_board
    # opp = 9223927819925454848 & Bits.on_board
    # my = 169295288
    # opp = 555783070679040

    my = sum([1 << i for i in [25, 35, 45]])
    opp = sum([1 << i for i in [22, 31, 32]])

    my = Player(my)
    opp = Player(opp)
    # b = Board(my, opp)
    # eval = Evaluation.evaluate(b)
    #
    # print(eval)
    # print(tobin(my))
    # print(tobin(op))
    # open_pos = (my ^ op) ^ ((2 ** 64) - 1)
    # get_board(my, op)
    # # get_board(open_pos, 0)
    # v = Evaluation()
    # # get_board(v.attack(my, open_pos), 0)
    # shift_type = Bits.shift_vertical
    # moves = get_moves(op, open_pos, shift_type)
    # unsafe_pieces = eaten_pieces(moves, shift_type)
    # get_board(moves, 0)
    #
    # get_board(rshift(open_pos, Bits.shift_vertical) & op, 0)
    # attackers = op
    # open_board = ((my ^ op) ^ ((2 ** 64) - 1)) & Bits.on_board
    # movetype = Bits.shift_vertical
    # moves = (attackers & rshift(open_board, movetype)) | (open_board & rshift(
    #     attackers, movetype))
    # get_board(0, open_board)
    # print(tobin(open_board))
    # m1 = attackers & rshift(open_board, movetype)
    # m2 = open_board & rshift(attackers, movetype)
    # # get_board(rshift(open_board, movetype), 0)
    # ff = ShowBoard(my, op)
    # print(ff)
    # get_board(my, op)
    # print(tobin(my), tobin(op))
    # get_board(m1, 0)
    # get_board(m2, 0)
    # # get_board(0, (rshift(open_board, movetype)))
    # # get_board((open_board & rshift(attackers, movetype)), 0)
