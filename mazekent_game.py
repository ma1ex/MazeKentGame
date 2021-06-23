"""
MazeKent game
"""

import arcade
import random


class MazeKent(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.tile_empty = 0
        self.tile_crate = 1

        # Maze size
        self.maze_width = 10
        self.maze_height = 10

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Create the maze
        maze = self.make_maze(self.maze_width, self.maze_height)
        [print(m) for m in maze]

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    # noinspection PyMethodMayBeStatic
    def run(self):
        """
        Run game

        :return:
        """

        arcade.run()

    def create_grid(self, width: int, height: int) -> list:

        grid = []

        for row in range(height):
            grid.append([])

            for column in range(width):
                if column % 2 == 1 and row % 2 == 1:
                    grid[row].append(self.tile_empty)
                elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                    grid[row].append(self.tile_crate)
                else:
                    grid[row].append(self.tile_crate)

        return grid

    def make_maze(self, maze_width: int, maze_height: int) -> list:

        maze = self.create_grid(maze_width, maze_height)

        [print(g) for g in maze]
        print()

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
                    maze[max(y, yy) * 2][x * 2 + 1] = self.tile_empty
                if yy == y:
                    maze[y * 2 + 1][max(x, xx) * 2] = self.tile_empty

                walk(xx, yy)

        walk(random.randrange(w), random.randrange(h))

        return maze
