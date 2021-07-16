import time
import traceback
import random


def create_grid(width: int, height: int) -> list:

    empty = 0
    crate = 1

    grid = []

    for row in range(height):
        grid.append([])

        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(empty)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(crate)
            else:
                grid[row].append(crate)

    return grid


def make_maze(maze_width: int, maze_height: int) -> list:

    maze = create_grid(maze_width, maze_height)

    # [print(g) for g in maze]
    # print()

    empty = 0
    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = empty
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = empty

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    return maze


def main():
    # Program timer
    start_time = time.time()
    print('> Creating...\n')

    try:
        # grid = create_grid(20, 20)
        # [print(g) for g in grid]

        maze = make_maze(20, 20)
        [print(m) for m in maze]

    except KeyboardInterrupt:
        print('\nWARNING: Interrupted by user!')

    except Exception as err:
        print('\nERROR: ', err)
        print(traceback.format_exc())

    finally:
        print('\n> Elapsed time:', time.time() - start_time)


if __name__ == '__main__':
    main()
