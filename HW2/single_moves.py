import collections
import helper


def get_single_move(positions, my_color, no_of_rows, no_of_cols):
    if my_color == "BLACK":
        my_color_symbol = 'B'
        base_camp = helper.black_base_camp
    else:
        my_color_symbol = 'W'
        base_camp = helper.white_base_camp

    pawns_outside = []
    pawns_inside = []

    for pawn in positions[my_color_symbol]:
        if pawn in base_camp:
            pawns_inside.append(pawn)
        else:
            pawns_outside.append(pawn)

    # if there is at least one pawn inside base camp
    if len(pawns_inside) != 0:
        inside_moves = []
        for pawn in pawns_inside:
            # get_all_moves_of_pawn_single returns to_states either outside and inside of base camp
            successors = get_all_moves_of_pawn_single(pawn, positions, no_of_rows, no_of_cols, my_color_symbol)
            for to_state in successors:
                if to_state not in base_camp:
                    return pawn, to_state
                else:
                    inside_moves.append((pawn, to_state))
        # comes here only when no pawns can go outside and they just have to move further away inside base camp
        if len(inside_moves) != 0:
            return inside_moves[0]

    # comes here when 1. no pawns inside base camp
    # 2. when all pawns in base camp cannot move outside or further away from base camp
    if len(pawns_outside) != 0:
        for pawn in pawns_outside:
            successors = get_all_moves_of_pawn_single(pawn, positions, no_of_rows, no_of_cols, my_color_symbol)
            if len(successors) != 0:
                return pawn, successors[0]


# return a list of legal possible moves(adjacent cells and hops the pawn could make)
def get_all_moves_of_pawn_single(pawn_cordinates, positions, no_of_rows, no_of_cols, player_color):
    y = pawn_cordinates[0]
    x = pawn_cordinates[1]
    adjacent_node_list = [(y - 1, x - 1), (y, x - 1), (y + 1, x - 1), (y + 1, x), (y + 1, x + 1), (y, x + 1),
                          (y - 1, x + 1), (y - 1, x)]

    adjacent_moves = []
    jump_moves = []

    queue = collections.deque([pawn_cordinates])
    visited = set()
    visited.add(pawn_cordinates)
    # add adjacent moves of pawn
    for node in adjacent_node_list:
        if 0 <= node[0] < no_of_cols and 0 <= node[1] < no_of_rows and node not in positions['W'] and node not in \
                positions['B']:
            adjacent_moves.append(node)
            visited.add(node)

    # add hop moves of pawn(includes pawn cordinate also)
    while queue:
        parent = queue.popleft()
        y, x = parent[0], parent[1]

        children = [(y - 1, x - 1), (y, x - 1), (y + 1, x - 1), (y + 1, x), (y + 1, x + 1), (y, x + 1), (y - 1, x + 1),
                    (y - 1, x)]
        grand_children = [(y - 2, x - 2), (y, x - 2), (y + 2, x - 2), (y + 2, x), (y + 2, x + 2), (y, x + 2),
                          (y - 2, x + 2), (y - 2, x)]

        for child in children:
            if 0 <= child[0] < no_of_cols and 0 <= child[1] < no_of_rows and (
                    child in positions['W'] or child in positions['B']):
                grand_child = grand_children[children.index(child)]
                if 0 <= grand_child[0] < no_of_cols and 0 <= grand_child[1] < no_of_rows and grand_child not in \
                        positions['W'] and grand_child not in positions['B'] and grand_child not in visited:
                    jump_moves.append(grand_child)
                    queue.append(grand_child)
                    visited.add(grand_child)

    all_possible_moves = adjacent_moves + jump_moves
    possible_legal_moves = filter_moves_single(pawn_cordinates, positions, all_possible_moves, player_color)
    return possible_legal_moves


def filter_moves_single(pawn, positions, all_possible_moves, player_color):
    legal_moves = []
    pawn_y = pawn[0]
    pawn_x = pawn[1]

    if player_color == 'B':
        if pawn in helper.black_base_camp:

            for move in all_possible_moves:
                if move not in helper.black_base_camp:
                    legal_moves.append(move)

            if len(legal_moves) == 0:
                base_camp_successors = [x for x in all_possible_moves if x in helper.black_base_camp]
                for to_state in base_camp_successors:
                    if to_state[0] >= pawn_y and to_state[1] >= pawn_x:
                        legal_moves.append(to_state)

        elif pawn in helper.white_base_camp:
            for move in all_possible_moves:
                if move in helper.white_base_camp:
                    legal_moves.append(move)

        else:  # black pawn in open area
            for move in all_possible_moves:
                if move not in helper.black_base_camp:
                    legal_moves.append(move)

    if player_color == 'W':
        if pawn in helper.white_base_camp:

            for move in all_possible_moves:
                if move not in helper.white_base_camp:
                    legal_moves.append(move)

            if len(legal_moves) == 0:
                base_camp_successors = [x for x in all_possible_moves if x in helper.white_base_camp]
                for to_state in base_camp_successors:
                    if to_state[0] <= pawn_y and to_state[1] <= pawn_x:
                        legal_moves.append(to_state)

        elif pawn in helper.black_base_camp:
            for move in all_possible_moves:
                if move in helper.black_base_camp:
                    legal_moves.append(move)

        else:  # white pawn in open area
            for move in all_possible_moves:
                if move not in helper.white_base_camp:
                    legal_moves.append(move)
    return legal_moves
