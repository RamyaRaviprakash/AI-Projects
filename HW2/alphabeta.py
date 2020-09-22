import helper

depth_limit = 2
flag = False


def set_depth_limit(d):
    global depth_limit
    depth_limit = d


def is_pawns_in_base_camp(f):
    global flag
    flag = f


def get_best_move_for_game(positions, my_color, no_of_rows, no_of_cols, time_left):
    if my_color == "BLACK":
        player_color = 'B'
        opponent_color = 'W'
    else:
        player_color = 'W'
        opponent_color = 'B'

    set_depth_limit(2)
    is_pawns_in_base_camp(False)

    pawns_in_base_camp = helper.get_all_pawns_in_base_camp(positions, player_color)
    if len(pawns_in_base_camp) > 0:
        set_depth_limit(3)
        is_pawns_in_base_camp(True)

    if time_left < 10:
        set_depth_limit(1)

    v, best_move = alpha_beta_search(positions, player_color, opponent_color, no_of_rows, no_of_cols)
    return best_move


def alpha_beta_search(positions, player_color, opponent_color, no_of_rows, no_of_cols):
    v, best_move = max_value(positions, float("-inf"), float("inf"), player_color, opponent_color, 0, no_of_rows,
                             no_of_cols)
    return v, best_move


def max_value(positions, alpha, beta, player_color, opponent_color, depth, no_of_rows, no_of_cols):
    if terminal_test(depth):
        return e_func(positions, player_color)

    v = float("-inf")
    moves = helper.get_all_moves_possible_from_given_state(positions, player_color, no_of_rows, no_of_cols)
    best_move = tuple()
    for pawn in moves:
        for to_state in moves[pawn]:
            new_v = \
                min_value(result(positions, player_color, pawn, to_state), alpha, beta, player_color,
                          opponent_color,
                          depth + 1, no_of_rows, no_of_cols)[0]

            if v < new_v:
                v = new_v
                best_move = (pawn, to_state)

            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
    return v, best_move


def min_value(positions, alpha, beta, player_color, opponent_color, depth, no_of_rows, no_of_cols):
    if terminal_test(depth):
        return e_func(positions, player_color)

    v = float("inf")
    moves = helper.get_all_moves_possible_from_given_state(positions, opponent_color, no_of_rows, no_of_cols)
    best_move = tuple()
    for pawn in moves:
        for to_state in moves[pawn]:
            new_v = \
                max_value(result(positions, opponent_color, pawn, to_state), alpha, beta, player_color, opponent_color,
                          depth + 1, no_of_rows, no_of_cols)[0]
            if new_v < v:
                v = new_v
                best_move = (pawn, to_state)
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
    return v, best_move


def terminal_test(depth):
    return depth == depth_limit


def e_func(positions, player_color):
    if flag:
        white_base_camp_empty_positions = [(15, 15)]
        black_base_camp_empty_positions = [(0, 0)]
    else:
        white_base_camp_empty_positions = [x for x in helper.white_base_camp if x not in positions['B']]
        black_base_camp_empty_positions = [x for x in helper.black_base_camp if x not in positions['W']]

    black_positions = positions['B']
    white_positions = positions['W']

    x = 0
    for black_position in black_positions:
        max_dist = 0
        # calculate distance from white base camp
        for empty_position in white_base_camp_empty_positions:
            max_dist = max(max_dist, distance_between(black_position, empty_position))
        x += max_dist

    y = 0
    for white_position in white_positions:
        max_dist = 0
        for empty_position in black_base_camp_empty_positions:
            max_dist = max(max_dist, distance_between(white_position, empty_position))
        y += max_dist

    if player_color == 'W':
        return x - y, None
    else:
        return y - x, None


def distance_between(p1, p2):
    return ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)


def result(positions, color, from_state, to_state):
    new_positions_white = positions['W'].copy()
    new_positions_black = positions['B'].copy()
    new_positions = {'W': new_positions_white, 'B': new_positions_black}
    if from_state in new_positions[color]:
        new_positions[color].remove(from_state)
        new_positions[color].append(to_state)
    return new_positions
