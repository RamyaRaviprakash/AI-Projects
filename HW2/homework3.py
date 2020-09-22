import collections
import helper
import alphabeta
import single_moves


def main():
    with open("input.txt") as f:
        scenario = f.readline().strip("\n")
        my_color = f.readline().strip("\n")
        time_left = float(f.readline().strip("\n"))
        grid = []

        for i in range(0, 16):
            grid.append(list(f.readline().strip("\n")))

        no_of_rows, no_of_cols = len(grid), len(grid)
        positions = helper.build_positions_from_grid(grid, no_of_rows, no_of_cols)

        if scenario == "SINGLE":
            helper.init_base_camp()
            best_move = single_moves.get_single_move(positions, my_color, no_of_rows, no_of_cols)
        else:
            helper.init_base_camp()
            best_move = alphabeta.get_best_move_for_game(positions, my_color, no_of_rows, no_of_cols, time_left)

        if is_adjacent(best_move):
            move_type = "E"
            move = [best_move[0], best_move[1]]
        else:
            move_type = "J"
            move = find_jump_path(best_move, positions, no_of_rows, no_of_cols)

        write_to_output(move, move_type)


def is_adjacent(final_move):
    from_y = final_move[0][0]
    from_x = final_move[0][1]
    to_y = final_move[1][0]
    to_x = final_move[1][1]

    adjacent_node_list = [(from_y - 1, from_x - 1), (from_y, from_x - 1), (from_y + 1, from_x - 1),
                          (from_y + 1, from_x), (from_y + 1, from_x + 1), (from_y, from_x + 1),
                          (from_y - 1, from_x + 1), (from_y - 1, from_x)]
    return (to_y, to_x) in adjacent_node_list


def write_to_output(move, move_type):
    with open("output.txt", "w") as f:
        output_str = ""
        if move_type == "E":
            output_str += move_type + " " + ",".join(map(str, move[0])) + " " + ",".join(map(str, move[1])) + "\n"
        else:
            for i in range(0, len(move) - 1):
                step = move[i]
                next_step = move[i + 1]
                output_str += move_type + " " + ",".join(map(str, step)) + " " + ",".join(map(str, next_step)) + "\n"
        output_str = output_str.rstrip("\n")
        f.write(output_str)


def find_jump_path(best_move, positions, no_of_rows, no_of_cols):
    source_cordinates = best_move[0]
    dest_cordinates = best_move[1]

    queue = collections.deque([[source_cordinates]])
    visited = set()
    visited.add(source_cordinates)

    adjacent_node_list = [(source_cordinates[0] - 1, source_cordinates[1] - 1),
                          (source_cordinates[0], source_cordinates[1] - 1),
                          (source_cordinates[0] + 1, source_cordinates[1] - 1),
                          (source_cordinates[0] + 1, source_cordinates[1]),
                          (source_cordinates[0] + 1, source_cordinates[1] + 1),
                          (source_cordinates[0], source_cordinates[1] + 1),
                          (source_cordinates[0] - 1, source_cordinates[1] + 1),
                          (source_cordinates[0] - 1, source_cordinates[1])]
    for node in adjacent_node_list:
        if 0 <= node[0] < no_of_cols and 0 <= node[1] < no_of_rows and node not in positions['W'] and node not in \
                positions['B']:
            visited.add(node)

    while queue:
        parent = queue.popleft()  # parent is a list containing path
        y, x = parent[len(parent) - 1][0], parent[len(parent) - 1][1]

        if parent[len(parent) - 1] == dest_cordinates:
            return parent

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
                    grand_child_path = parent + [grand_child]
                    queue.append(grand_child_path)
                    visited.add(grand_child)


if __name__ == "__main__":
    main()
