import homework3
import time


def main():
    # grid = read_from_file()

    grid = [['B', 'B', 'B', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['B', 'B', 'B', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['B', 'B', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['B', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W']]

    # grid = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]

    # homework3.main(grid, "BLACK")
    # return
    count = 0
    turn_number = 0

    # 16x16
    endCondition = (grid[0][0] == grid[1][0] == grid[2][0] == grid[3][0] == grid[4][0] ==
                    grid[0][1] == grid[1][1] == grid[2][1] == grid[3][1] == grid[4][1] ==
                    grid[0][2] == grid[1][2] == grid[2][2] == grid[3][2] ==
                    grid[0][3] == grid[1][3] == grid[2][3] ==
                    grid[0][4] == grid[1][4] == 'W') \
                   or (grid[15][15] == grid[14][15] == grid[13][15] == grid[12][15] == grid[11][15] ==
                       grid[15][14] == grid[14][14] == grid[13][14] == grid[12][14] == grid[11][14] ==
                       grid[15][13] == grid[14][13] == grid[13][13] == grid[12][13] ==
                       grid[15][12] == grid[14][12] == grid[13][12] ==
                       grid[15][11] == grid[14][11] == 'B')
    start_time = time.time()
    # print("start time: ", start_time)
    black_time_left = 300
    white_time_left = 300
    while not endCondition:
        if count % 2 == 0:
            my_color = 'BLACK'
            player = 'B'
            time_left = black_time_left
        else:
            my_color = 'WHITE'
            player = 'W'
            time_left = white_time_left

        move_start_time = time.time()
        best_move = homework3.main_for_master(grid, my_color, time_left)
        move_end_time = time.time()
        time_taken = move_end_time - move_start_time

        if player == 'B':
            black_time_left = black_time_left - time_taken
        else:
            white_time_left = white_time_left - time_taken
        turn_number += 1
        print("turn number: ", turn_number)
        print("time taken till now: ", move_end_time - start_time)

        if len(best_move) == 0:
            print("hi")
            break

        if len(best_move) != 0:
            from_y = best_move[0][0]
            from_x = best_move[0][1]
            to_y = best_move[1][0]
            to_x = best_move[1][1]

            grid[from_x][from_y] = '.'
            grid[to_x][to_y] = player

            f9 = open("checker.txt", "w")
            for i in range(0, len(grid)):
                for j in range(0, len(grid)):
                    f9.write(grid[i][j])
                f9.write("\n")
            count += 1
            f9.close()
            # time.sleep(2)
    print("end time: ", time.time())
    print("took seconds: ", time.time() - start_time)


def print_grid(grid):
    for i in range(0, len(grid)):
        outstr = ""
        for j in range(0, len(grid)):
            outstr += grid[i][j]
        print(outstr)
        print("\n")


def read_from_file():
    f2 = open("example.txt", "r")
    grid = []

    for i in range(0, 16):
        grid.append(list(f2.readline().strip("\n")))
    return grid


if __name__ == "__main__":
    main()
