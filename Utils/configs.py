list_moves = [10, 1, 11, 9]
list_slant = [11, 9]
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

left_control = 171865964544
right_control = 10741622784
center_control = 42966491136

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

depth_adjustment = 40

debug = False
logging = False
# debug = True

dict_fortress = {'sm_left': 281887696617728,
                 'lg_left': 493097109127616,
                 'sm_right': 1102736002049,
                 'lg_right': 7712703265799}

dict_guard = {'sm_left': 206225735680,
              'lg_left': 51657097216,
              'sm_right': 2151680000,
              'lg_right': 25799188480}

dict_attack = {'sm_left': 105553149821024,
               'lg_left': 26388287455256,
               'sm_right': 13194143727628,
               'lg_right': 52776591687728}

won_position = 10000
decrementable = 5000
ply = 10
ply_decrement = 1

# Principal Variation Search
pvs = True


# board ply
forced_move_extension = 5
forced_capture_extension = 10
endgame_capture_extension = 5
forced_endgame_capture = 10
multiple_capture_extension = 7
early_pass_extension = 10


# Evaluation Type
eval_upper_bound = 0
eval_lower_bound = 1
eval_exact = 2


ratios_eval = ratios = [2147483647] + [int(300 / (i + 1)) for i in range(64)]
