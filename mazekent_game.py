"""
MazeKent game
"""
import timeit
import arcade
import random
from typing import (
    List
)


class MazeKent(arcade.Window):
    """
    Main application class
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Window size
        self.screen_width = width
        self.screen_height = height

        self.physics_engine = None

        # Fill maze
        self.tile_empty = 0
        self.tile_crate = 1

        # Maze default size
        self.maze_width = 10
        self.maze_height = 10

        # Sprites config
        self.native_sprite_size = 128
        self.sprite_scaling = 0.40
        self.sprite_size = self.native_sprite_size * self.sprite_scaling

        # Sprites
        self.sprite_wall = r'data/images/tiles/brickTextureWhite.png'
        self.sprite_map_viewer = r'data/images/tiles/circle.png'
        self.map_viewer = None

        # Sprite lists
        self.wall_list = None
        self.map_viewer_list = None

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Sprite lists init
        self.wall_list = arcade.SpriteList()
        self.map_viewer_list = arcade.SpriteList()

        # Create the maze
        maze = self.make_maze(self.maze_width, self.maze_height)

        for row in range(self.maze_height):
            for column in range(self.maze_width):
                if maze[row][column] == 1:
                    wall = arcade.Sprite(self.sprite_wall, self.sprite_scaling)
                    wall.center_x = column * self.sprite_size + self.sprite_size / 2
                    wall.center_y = row * self.sprite_size + self.sprite_size / 2
                    self.wall_list.append(wall)

        # Set up the map_viewer
        self.map_viewer = arcade.Sprite(self.sprite_map_viewer)
        self.map_viewer_list.append(self.map_viewer)

        # Set map_viewer position
        self.map_viewer.center_x = 0
        self.map_viewer.center_y = 0

        # self.physics_engine = arcade.PhysicsEngineSimple(arcade.Sprite(), self.wall_list)
        self.physics_engine = arcade.PhysicsEngineSimple(self.map_viewer, arcade.SpriteList())

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        print(f'Total wall blocks: {len(self.wall_list)}')

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # self.player_test = arcade.draw_circle_filled(self.p_x, self.p_y, 20, arcade.color.GOLD)

        # Call draw() on all your sprite lists below
        self.wall_list.draw()
        self.map_viewer_list.draw()

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        start_time = timeit.default_timer()

        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + 200
        if self.map_viewer.left < left_bndry:
            self.view_left -= left_bndry - self.map_viewer.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + self.screen_width - 200
        if self.map_viewer.right > right_bndry:
            self.view_left += self.map_viewer.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + self.screen_height - 200
        if self.map_viewer.top > top_bndry:
            self.view_bottom += self.map_viewer.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + 200
        if self.map_viewer.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.map_viewer.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                self.screen_width + self.view_left,
                                self.view_bottom,
                                self.screen_height + self.view_bottom)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """

        # if key == arcade.key.UP:
        #     # self.p_y += self.player_test_step
        #     # self.player_test_move = True
        #     self.map_viewer.change_y = 25
        # elif key == arcade.key.DOWN:
        #     # self.p_y -= self.player_test_step
        #     # self.player_test_move = True
        #     self.map_viewer.change_y = -25
        # elif key == arcade.key.LEFT:
        #     # self.p_x -= self.player_test_step
        #     # self.player_test_move = True
        #     self.map_viewer.change_x = -25
        # elif key == arcade.key.RIGHT:
        #     # self.p_x += self.player_test_step
        #     # self.player_test_move = True
        #     self.map_viewer.change_x = 25

        if key == arcade.key.W:
            # self.p_y += self.player_test_step
            # self.player_test_move = True
            self.map_viewer.change_y = 30
        elif key == arcade.key.S:
            # self.p_y -= self.player_test_step
            # self.player_test_move = True
            self.map_viewer.change_y = -30
        elif key == arcade.key.A:
            # self.p_x -= self.player_test_step
            # self.player_test_move = True
            self.map_viewer.change_x = -30
        elif key == arcade.key.D:
            # self.p_x += self.player_test_step
            # self.player_test_move = True
            self.map_viewer.change_x = 30

        elif key == arcade.key.M:
            # print('"M" key was pressed!')
            self.show_full_map()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        # self.player_test_move = False

        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.map_viewer.change_y = 0
        # elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
        #     self.map_viewer.change_x = 0

        if key == arcade.key.W or key == arcade.key.S:
            self.map_viewer.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.map_viewer.change_x = 0

        elif key == arcade.key.M:
            self.show_full_map(release=True)

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

    def create_grid(self, width: int, height: int) -> List[List[int]]:
        """
        Generated base grid

        :param width: grid width (use odd value!)
        :param height: grid height (use odd value!)

        :return: base grid
        """

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

    def make_maze(self, maze_width: int, maze_height: int) -> List[List[int]]:
        """
        Generating a random maze based on a basic grid method `create_grid()`

        :param maze_width: maze width (use odd value!)
        :param maze_height: maze height (use odd value!)

        :return: completed maze
        """

        maze = self.create_grid(maze_width, maze_height)

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

    def show_full_map(self, release: bool = False) -> None:
        """
        Display of the whole map

        :param release: key status: pressed or not

        :return: None
        """

        if not release:
            arcade.set_viewport(0, self.screen_width * self._get_screen_ratio(),
                                0, self.screen_height * self._get_screen_ratio(),)
        else:
            arcade.set_viewport(
                self.view_left,
                self.screen_width + self.view_left,
                self.view_bottom,
                self.screen_height + self.view_bottom
            )

    def _get_screen_ratio(self) -> float:
        """
        Screen to labyrinth size ratio

        :return: ratio
        """

        ratio = 0.0

        if self.screen_height < self.screen_width and self.maze_width > self.maze_height:
            ratio = (self.sprite_size * self.maze_width) / self.screen_width
            # print('1 cond')
        elif self.screen_height < self.screen_width and self.maze_width < self.maze_height:
            ratio = (self.sprite_size * self.maze_height) / self.screen_height
            # print('2 cond')
        elif self.screen_height < self.screen_width and self.maze_width == self.maze_height:
            ratio = (self.sprite_size * self.maze_width) / self.screen_height
            # print('3 cond')

        elif self.screen_height > self.screen_width and self.maze_height > self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_height
            # print('4 cond')
        elif self.screen_height > self.screen_width and self.maze_height < self.maze_width:
            ratio = (self.sprite_size * self.maze_width) / self.screen_width
            # print('5 cond')
        elif self.screen_height > self.screen_width and self.maze_height == self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            # print('6 cond')

        elif self.screen_height == self.screen_width and self.maze_height > self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            # print('7 cond')
        elif self.screen_height == self.screen_width and self.maze_height < self.maze_width:
            ratio = (self.sprite_size * self.maze_width) / self.screen_height
            # print('8 cond')
        elif self.screen_height == self.screen_width and self.maze_height == self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            # print('9 cond')

        print(f'{ratio = }')

        return ratio
