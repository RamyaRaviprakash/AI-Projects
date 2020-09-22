import collections

black_base_camp = {}
white_base_camp = {}


def init_base_camp():
    global black_base_camp
    global white_base_camp
    black_base_camp = {
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2),
        (0, 3), (1, 3), (2, 3), (0, 4), (1, 4)}
    white_base_camp = {
        (14, 11), (15, 11), (13, 12), (14, 12), (15, 12), (12, 13), (13, 13), (14, 13), (15, 13), (11, 14), (12, 14),
        (13, 14), (14, 14), (15, 14), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)}


def get_all_pawns_in_base_camp(positions, pawn_color):
    base_camp = get_base_camp(pawn_color)
    pawns_in_base_camp = []
    for pawn in positions[pawn_color]:
        if pawn in base_camp:
            pawns_in_base_camp.append(pawn)
    return pawns_in_base_camp


def get_base_camp(pawn_color):
    if pawn_color == 'B':
        return black_base_camp
    else:
        return white_base_camp


# return all possible moves for a player(myself or opponent) for a given state of board
def get_all_moves_possible_from_given_state(positions, pawn_color, no_of_rows, no_of_cols):
    # if at least one pawn in base camp
    pawns_in_base_camp = get_all_pawns_in_base_camp(positions, pawn_color)
    if len(pawns_in_base_camp) != 0:
        outer_base_camp_moves = {}
        inner_base_camp_moves = {}
        for pawn in pawns_in_base_camp:
            pawn_moves = get_all_moves_of_pawn(pawn, positions, no_of_rows, no_of_cols, pawn_color)
            for to_state in pawn_moves:
                if to_state not in get_base_camp(pawn_color):
                    if pawn in outer_base_camp_moves:
                        outer_base_camp_moves[pawn].append(to_state)
                    else:
                        outer_base_camp_moves[pawn] = [to_state]
                else:
                    if pawn in inner_base_camp_moves:
                        inner_base_camp_moves[pawn].append(to_state)
                    else:
                        inner_base_camp_moves[pawn] = [to_state]
        if len(outer_base_camp_moves) != 0:
            return outer_base_camp_moves
        elif len(inner_base_camp_moves) != 0:
            return inner_base_camp_moves
        else:
            possible_moves = {}
            for pawn in positions[pawn_color]:
                pawn_moves = get_all_moves_of_pawn(pawn, positions, no_of_rows, no_of_cols, pawn_color)
                possible_moves[pawn] = pawn_moves
            return possible_moves

    # if no pawns in base camp
    else:
        possible_moves = {}
        for pawn in positions[pawn_color]:
            pawn_moves = get_all_moves_of_pawn(pawn, positions, no_of_rows, no_of_cols, pawn_color)
            possible_moves[pawn] = pawn_moves
        return possible_moves


# return a list of legal possible moves(adjacent cells and hops the pawn could make)
def get_all_moves_of_pawn(pawn_cordinates, positions, no_of_rows, no_of_cols, pawn_color):
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

    all_possible_moves = jump_moves + adjacent_moves
    possible_legal_moves = filter_moves(pawn_cordinates, positions, all_possible_moves, pawn_color)
    return possible_legal_moves


def filter_moves(pawn, positions, all_possible_moves, pawn_color):
    legal_moves = []
    pawn_y = pawn[0]
    pawn_x = pawn[1]
    if pawn_color == 'B':
        if pawn in black_base_camp:
            for move in all_possible_moves:
                if move not in black_base_camp:
                    legal_moves.append(move)

            if len(legal_moves) == 0:
                base_camp_successors = [x for x in all_possible_moves if x in black_base_camp]
                for to_state in base_camp_successors:
                    if to_state[0] >= pawn_y and to_state[1] >= pawn_x:
                        legal_moves.append(to_state)

        elif pawn in white_base_camp:
            for move in all_possible_moves:
                if move in white_base_camp:
                    legal_moves.append(move)

        else:  # black pawn in open area
            for move in all_possible_moves:
                if move not in black_base_camp:
                    legal_moves.append(move)

    if pawn_color == 'W':
        if pawn in white_base_camp:
            for move in all_possible_moves:
                if move not in white_base_camp:
                    legal_moves.append(move)

            if len(legal_moves) == 0:
                base_camp_successors = [x for x in all_possible_moves if x in white_base_camp]
                for to_state in base_camp_successors:
                    if to_state[0] <= pawn_y and to_state[1] <= pawn_x:
                        legal_moves.append(to_state)

        elif pawn in black_base_camp:
            for move in all_possible_moves:
                if move in black_base_camp:
                    legal_moves.append(move)

        else:  # white pawn in open area
            for move in all_possible_moves:
                if move not in white_base_camp:
                    legal_moves.append(move)

    return legal_moves


def build_positions_from_grid(grid, no_of_rows, no_of_cols):
    positions = {'W': [], 'B': []}
    for i in range(0, no_of_rows):
        for j in range(0, no_of_cols):
            if grid[i][j] == 'W':
                positions['W'].append((j, i))
            elif grid[i][j] == 'B':
                positions['B'].append((j, i))
    return positions
