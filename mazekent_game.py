"""
MazeKent game
"""
import timeit
import arcade
import random
from typing import (
    List
)


class PlayerCharacter(arcade.Sprite):
    """
    Player class
    """

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.updates_per_frame = 3  # Temporarily hardcoded

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.cur_idle_texture = 0

        self.scale = 0.9  # Temporarily hardcoded

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.points = [[-2, -34], [18, 0], [0, 0], [-16, 18]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = 'data/images/tiles/characters/hero/hero'  # Temporarily hardcoded

        # Load textures for idle standing
        self.idle_texture = arcade.load_texture(f'{main_path}_idle.png')

        # Load textures for walking
        self.walk_top_textures = [arcade.load_texture(f'{main_path}_walk_top{i}.png') for i in range(9)]
        self.walk_down_textures = [arcade.load_texture(f'{main_path}_walk_down{i}.png') for i in range(9)]
        self.walk_left_textures = [arcade.load_texture(f'{main_path}_walk_left{i}.png') for i in range(9)]
        self.walk_right_textures = [arcade.load_texture(f'{main_path}_walk_right{i}.png') for i in range(9)]

    def update_animation(self, delta_time: float = 1/60):

        # self.cur_texture += 1
        # if self.cur_texture > 7 * self.updates_per_frame:
        #     self.cur_texture = 0
        # frame = self.cur_texture // self.updates_per_frame
        # direction = self.character_face_direction
        # self.texture = self.walk_down_textures[frame][direction]

        # Idle animation

        # Stoped
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture
            return

        # Left
        if self.change_x < 0:
            self.walk_character(self.walk_left_textures)

        # Right
        if self.change_x > 0:
            self.walk_character(self.walk_right_textures)

        # Down
        elif self.change_y < 0:
            self.walk_character(self.walk_down_textures)

        # Top
        elif self.change_y > 0:
            self.walk_character(self.walk_top_textures)

    def walk_character(self, texture_list: list) -> None:
        """
        Walking animation

        :param texture_list: texture list
        :return: None
        """
        self.cur_texture += 1

        if self.cur_texture > 7 * self.updates_per_frame:
            self.cur_texture = 0

        frame = self.cur_texture // self.updates_per_frame
        self.texture = texture_list[frame]

    # noinspection PyMethodMayBeStatic
    def load_texture_pair(self, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """

        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]


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
        self.score = 0

        # Fill maze
        self.tile_empty = 0
        self.tile_crate = 1

        # Maze default size
        self.maze_width = 11
        self.maze_height = 11

        # Sprites config
        self.native_sprite_size = 32  # 128
        self.sprite_scaling = 1.7     # 0.40
        self.sprite_size = self.native_sprite_size * self.sprite_scaling

        # Sprites --------------------------------------------------------------

        # Walls
        # self.sprite_wall = r'data/images/tiles/brickTextureWhite.png'
        self.sprite_wall = r'data/images/tiles/wall/wall_labyrinth_style1_i.png'
        self.sprite_wall_list = [
            r'data/images/tiles/wall/wall_labyrinth_style1_a.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_g.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_i.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_k.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_l.png',
        ]

        # Floor
        self.sprite_floor = r'data/images/tiles/floor_metal_b.png'
        self.sprite_floor_list = [
            r'data/images/tiles/floor/floor_labyrinth_undamaged_c.png',
            r'data/images/tiles/floor/floor_labyrinth_undamaged_e.png',
            r'data/images/tiles/floor/floor_labyrinth_undamaged_i.png',
            r'data/images/tiles/floor/floor_labyrinth_undamaged_k.png',
            r'data/images/tiles/floor/floor_labyrinth_undamaged_l.png',
        ]

        # Player
        self.player_sprite = None

        # Items
        self.item_chip = r'data/images/tiles/items/battery_nucleus.png'

        # Exit level
        self.exit_sprite = None

        # Debug player
        self.sprite_map_viewer = r'data/images/tiles/circle.png'
        self.map_viewer = None

        # Sprite lists ---------------------------------------------------------
        self.wall_list = None
        self.floor_list = None
        self.map_viewer_list = None
        self.player_list = None
        self.items_list = None

        # Available floor coords - for place game objects
        self.unused_coords_list = []
        self.player_start_coords = None
        self.exit_start_coords = None

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Background color
        # arcade.set_background_color(arcade.color.AMAZON)
        arcade.set_background_color((50, 50, 50))

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Sprite lists init
        # self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        # self.map_viewer_list = arcade.SpriteList()
        self.items_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Create the maze
        maze = self.make_maze(self.maze_width, self.maze_height)
        # [print(i) for i in maze]

        # Generate walls and floor
        for row in range(self.maze_height):
            for column in range(self.maze_width):
                if maze[row][column] == 1:
                    wall = arcade.Sprite(random.choice(self.sprite_wall_list), self.sprite_scaling)
                    wall.center_x = column * self.sprite_size + self.sprite_size / 2
                    wall.center_y = row * self.sprite_size + self.sprite_size / 2
                    self.wall_list.append(wall)
                else:
                    # Add unused coords for place mics items
                    self.unused_coords_list.append((
                        column * self.sprite_size + self.sprite_size / 2,
                        row * self.sprite_size + self.sprite_size / 2
                    ))

                    # floor = arcade.Sprite(self.sprite_floor, self.sprite_scaling)
                    floor = arcade.Sprite(random.choice(self.sprite_floor_list), self.sprite_scaling)
                    floor.center_x = column * self.sprite_size + self.sprite_size / 2
                    floor.center_y = row * self.sprite_size + self.sprite_size / 2
                    self.floor_list.append(floor)

        # print()
        # [print(i) for i in self.unused_coords_list]

        # Set up the map_viewer ------------------------------------------------
        # self.map_viewer = arcade.Sprite(self.sprite_map_viewer)
        # self.map_viewer_list.append(self.map_viewer)
        #
        # # Set map_viewer position
        # self.map_viewer.center_x = 0
        # self.map_viewer.center_y = 0

        # Set up the player ----------------------------------------------------
        self.player_sprite = PlayerCharacter()
        self.player_list.append(self.player_sprite)

        # Start position
        # Calculating the player's starting position from the `self.unused_coords_list()`
        player_coords_idx = self.unused_coords_list.index(max([i for i in self.unused_coords_list]))
        self.player_start_coords = self.unused_coords_list.pop(player_coords_idx)
        # self.player_sprite.center_x = self.maze_width * self.sprite_size - 80
        # self.player_sprite.center_y = self.maze_height * self.sprite_size - 75
        self.player_sprite.center_x = self.player_start_coords[0]
        self.player_sprite.center_y = self.player_start_coords[1]

        # Checking for collision with a wall at the starting position
        # placed = False
        # while not placed:
        #
        #     # Are we in a wall?
        #     walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
        #     if len(walls_hit) == 0:
        #         # Not in a wall! Success!
        #         placed = True
        #     else:
        #         self.player_sprite.center_x -= 1
        #         self.player_sprite.center_y -= 1

        # Setup Exit current level objet ---------------------------------------
        # Calculating the exit's starting position from the `self.unused_coords_list()`
        exit_coords_idx = self.unused_coords_list.index(min([i for i in self.unused_coords_list]))
        self.exit_start_coords = self.unused_coords_list.pop(exit_coords_idx)
        # Set up the Exit level
        self.exit_sprite = arcade.Sprite(self.sprite_map_viewer, 0.6)
        self.exit_sprite.center_x = self.exit_start_coords[0]
        self.exit_sprite.center_y = self.exit_start_coords[1]

        # Setup items ----------------------------------------------------------
        random.shuffle(self.unused_coords_list)
        random.shuffle(self.unused_coords_list)

        count_items = 3
        if len(self.unused_coords_list) >= count_items:
            for item in range(count_items):
                x, y = self.unused_coords_list.pop()
                print(x, y)
                device = arcade.Sprite(self.item_chip, 0.12)
                device.center_x = x
                device.center_y = y
                self.items_list.append(device)

        # Setup physics engine -------------------------------------------------
        # self.physics_engine = arcade.PhysicsEngineSimple(self.map_viewer, arcade.SpriteList())
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        # Debug info -----------------------------------------------------------
        print(f'Total wall blocks: {len(self.wall_list)}')
        print(f'Total floor blocks: {len(self.floor_list)}')
        print(f'Total blocks: {len(self.wall_list) + len(self.floor_list)}')

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
        self.floor_list.draw()
        # self.map_viewer_list.draw()
        self.items_list.draw()
        self.player_list.draw()
        self.exit_sprite.draw()

        # Put the text on the screen.
        output = f'Score: {self.score}'
        arcade.draw_text(output,
                         self.view_left + 20,
                         self.screen_height - 20 + self.view_bottom,
                         arcade.color.WHITE, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        start_time = timeit.default_timer()

        self.physics_engine.update()

        # Update the players animation
        self.player_list.update_animation()

        # Collisions with items
        battery_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.items_list)

        for item in battery_hit_list:
            item.kill()
            self.score += 1

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # # Scroll left
        # left_bndry = self.view_left + 200
        # if self.map_viewer.left < left_bndry:
        #     self.view_left -= left_bndry - self.map_viewer.left
        #     changed = True
        #
        # # Scroll right
        # right_bndry = self.view_left + self.screen_width - 200
        # if self.map_viewer.right > right_bndry:
        #     self.view_left += self.map_viewer.right - right_bndry
        #     changed = True
        #
        # # Scroll up
        # top_bndry = self.view_bottom + self.screen_height - 200
        # if self.map_viewer.top > top_bndry:
        #     self.view_bottom += self.map_viewer.top - top_bndry
        #     changed = True
        #
        # # Scroll down
        # bottom_bndry = self.view_bottom + 200
        # if self.map_viewer.bottom < bottom_bndry:
        #     self.view_bottom -= bottom_bndry - self.map_viewer.bottom
        #     changed = True
        #
        # if changed:
        #     arcade.set_viewport(self.view_left,
        #                         self.screen_width + self.view_left,
        #                         self.view_bottom,
        #                         self.screen_height + self.view_bottom)

        # Scroll left
        left_bndry = self.view_left + 200
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + self.screen_width - 200
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + self.screen_height - 200
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + 200
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
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

        if key == arcade.key.UP:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -5
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5

        if key == arcade.key.W:
            self.player_sprite.change_y = 5
        elif key == arcade.key.S:
            self.player_sprite.change_y = -5
        elif key == arcade.key.A:
            self.player_sprite.change_x = -5
        elif key == arcade.key.D:
            self.player_sprite.change_x = 5

        # if key == arcade.key.W:
        #     self.map_viewer.change_y = 30
        # elif key == arcade.key.S:
        #     self.map_viewer.change_y = -30
        # elif key == arcade.key.A:
        #     self.map_viewer.change_x = -30
        # elif key == arcade.key.D:
        #     self.map_viewer.change_x = 30

        # "M" key for view full map
        elif key == arcade.key.M:
            self.show_full_map()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

        # if key == arcade.key.W or key == arcade.key.S:
        #     self.map_viewer.change_y = 0
        # elif key == arcade.key.A or key == arcade.key.D:
        #     self.map_viewer.change_x = 0

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
