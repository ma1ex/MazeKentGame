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
        self.teleport_textures = [arcade.load_texture(f'{main_path}_teleport{i}.png') for i in range(10)]

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
        elif self.change_x < 0:
            self.walk_character(self.walk_left_textures)

        # Right
        elif self.change_x > 0:
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

        if self.cur_texture > 8 * self.updates_per_frame:
            self.cur_texture = 0

        frame = self.cur_texture // self.updates_per_frame
        self.texture = texture_list[frame]

    def teleport(self):

        self.cur_texture += 1

        if self.cur_texture > 9 * self.updates_per_frame:
            return

        frame = self.cur_texture // self.updates_per_frame
        self.texture = self.teleport_textures[frame]


class ExitItem(arcade.Sprite):
    """
    Level Item exit class
    """

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.updates_per_frame = 7  # Temporarily hardcoded

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.cur_idle_texture = 0

        self.scale = 1  # Temporarily hardcoded

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.points = [[-2, -34], [18, 0], [0, 0], [-16, 18]]

        # --- Load Textures ---

        # Images from opengameart.org's Denzi SciFi Pack
        main_path = 'data/images/tiles/portal/portal'  # Temporarily hardcoded

        # Load textures for idle standing
        self.idle_texture = arcade.load_texture(f'{main_path}_off.png')

        # Load textures for animation
        self.exit_on_textures = [arcade.load_texture(f'{main_path}_on_{i}.png') for i in range(3)]

    def update_animation(self, delta_time: float = 1/60):

        self.cur_texture += 1
        if self.cur_texture > 2 * self.updates_per_frame:
            self.cur_texture = 0

        frame = self.cur_texture // self.updates_per_frame
        self.texture = self.exit_on_textures[frame]


class BatteryItem(arcade.Sprite):
    """
    Battery Item class
    """

    def __init__(self, idle_only=False):

        # Set up parent class
        super().__init__()

        self.updates_per_frame = 7  # Temporarily hardcoded

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.cur_idle_texture = 0

        self.scale = 0.12  # Temporarily hardcoded

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.points = [[-2, -34], [18, 0], [0, 0], [-16, 18]]

        # --- Load Textures ---

        # Original game textures Pack
        main_path = r'data/images/tiles/items/battery/battery'  # Temporarily hardcoded

        # Load textures for idle standing
        self.idle_texture = arcade.load_texture(f'{main_path}_off.png')

        # self.texture = self.idle_texture  # <- TEMP

        # Load textures for animation
        if idle_only:
            self.texture = self.idle_texture
        else:
            self.battery_textures = [arcade.load_texture(f'{main_path}_{i}.png') for i in range(6)]

    def update_animation(self, delta_time: float = 1/60):

        self.cur_texture += 1
        if self.cur_texture > 5 * self.updates_per_frame:
            self.cur_texture = 0

        frame = self.cur_texture // self.updates_per_frame
        self.texture = self.battery_textures[frame]

    def idle(self):
        self.texture = self.idle_texture


class MazeKent(arcade.Window):
    """
    Main application class
    """

    def __init__(self, width: int, height: int, title: str, maze_width: int = 11,
                 maze_height: int = 11):
        super().__init__(width, height, title)

        # Window size
        self.screen_width = width
        self.screen_height = height

        self.physics_engine = None
        self.score = 0
        self.of_score = 3
        self.game_over = False

        # Fill maze
        self.tile_empty = 0
        self.tile_crate = 1

        # Maze default size
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = None

        # Sprites config
        self.native_sprite_size = 32  # 128
        self.sprite_scaling = 1.7     # 0.40
        self.sprite_size = self.native_sprite_size * self.sprite_scaling

        # Minimap size & position
        self.minimap = None
        self.minimap_sprates_list = []
        self.minimap_native_sprite_size = 1  # 1  # 4
        self.minimap_sprite_scaling = 7      # 7  # 1.5
        self.minimap_sprite_size = self.minimap_native_sprite_size * self.minimap_sprite_scaling
        self.minimap_width = self.minimap_sprite_size * self.maze_width
        self.minimap_height = self.minimap_sprite_size * self.maze_height
        self.minimap_x = self.screen_width - self.minimap_width / 2 - 5
        self.minimap_y = self.minimap_height / 2 + 5
        self.show_minimap = False
        print(f'{self.minimap_sprite_size = }')
        print(f'{self.minimap_width = }')
        print(f'{self.minimap_height = }')
        print(f'{self.minimap_x = }')
        print(f'{self.minimap_y = }')

        # Sprites --------------------------------------------------------------

        # Walls
        self.sprite_wall_list = [
            r'data/images/tiles/wall/wall_labyrinth_style1_a.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_g.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_i.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_k.png',
            r'data/images/tiles/wall/wall_labyrinth_style1_l.png',
        ]

        # Floor
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
        self.items_coords_list = []
        self.battery_coords_list = []

        # Exit level
        self.exit_sprite = None

        # Items bar
        self.items_bar = None
        self.items_bar_battery = BatteryItem(idle_only=True)

        # Static minimap
        self.minimap_sprite = r'data/images/tiles/teal_square.png'
        # self.minimap_sprite = r'.ignored/red_square.png'
        self.minimap_exit_sprite = arcade.Sprite(r'data/images/tiles/lime_square.png', scale=4)
        self.minimap_item_sprite = arcade.Sprite(r'.ignored/yellow_square.png', scale=4)
        self.minimap_items_list = None

        # Debug player
        self.sprite_map_viewer = r'data/images/tiles/circle.png'
        self.map_viewer = None

        # Sprite lists ---------------------------------------------------------
        self.wall_list = None
        self.floor_list = None
        self.map_viewer_list = None
        self.player_list = None
        self.items_list = None
        self.exit_list = None
        self.minimap_list = None

        # Available floor coords - for place game objects
        self.unused_coords_list = []
        self.player_start_coords = None
        self.exit_start_coords = None

        # Viewport -------------------------------------------------------------

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Minimap
        self.program = None
        self.color_attachment = None
        self.offscreen = None
        self.quad_fs = None
        self.mini_map_quad = None

        # Background color and image
        arcade.set_background_color((0, 0, 0))
        self.background = None

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Background image
        self.background = arcade.load_texture(r'data/images/background/space.jpg')

        # Sprite lists init
        self.wall_list = arcade.SpriteList(is_static=True)
        self.floor_list = arcade.SpriteList(is_static=True)
        self.items_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.minimap_list = arcade.SpriteList(is_static=True)
        self.minimap_items_list = arcade.SpriteList(is_static=True)

        # Create the maze
        self.maze = self.make_maze(self.maze_width, self.maze_height)
        # [print(i) for i in maze]
        # maze_coords = []
        # for r in range(self.maze_height):
        #     for c in range(self.maze_width):
        #         maze_coords.append((c * self.sprite_size + self.sprite_size / 2,
        #         r * self.sprite_size + self.sprite_size / 2))
        # [print(i) for i in maze_coords]

        # Generate walls and floor
        for row in range(self.maze_height):
            for column in range(self.maze_width):
                if self.maze[row][column] == 1:
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

        # Set up the player ----------------------------------------------------
        self.player_sprite = PlayerCharacter()
        self.player_list.append(self.player_sprite)

        # Start position
        # Calculating the player's starting position from the `self.unused_coords_list()`
        player_coords_idx = self.unused_coords_list.index(max([i for i in self.unused_coords_list]))
        self.player_start_coords = self.unused_coords_list.pop(player_coords_idx)
        self.player_sprite.center_x = self.player_start_coords[0]
        self.player_sprite.center_y = self.player_start_coords[1]

        # Setup Exit current level objet ---------------------------------------
        # Calculating the exit's starting position from the `self.unused_coords_list()`
        self.exit_sprite = ExitItem()
        self.exit_list.append(self.exit_sprite)
        exit_coords_idx = self.unused_coords_list.index(min([i for i in self.unused_coords_list]))
        self.exit_start_coords = self.unused_coords_list.pop(exit_coords_idx)
        print(f'{self.exit_start_coords = }')

        self.exit_sprite.center_x = self.exit_start_coords[0]
        self.exit_sprite.center_y = self.exit_start_coords[1]

        # Setup items ----------------------------------------------------------
        random.shuffle(self.unused_coords_list)
        random.shuffle(self.unused_coords_list)

        # Generate Items
        if len(self.unused_coords_list) >= self.of_score:
            for item in range(self.of_score):
                x, y = self.unused_coords_list.pop()
                # print(f'Battery coords: {x=}, {y=}')
                battery = BatteryItem()
                battery.center_x = x
                battery.center_y = y
                self.items_list.append(battery)

                # Battery coords for use in minimap
                self.battery_coords_list.append((x, y))
        else:
            self.of_score = len(self.unused_coords_list) - 2
        print(f'{self.battery_coords_list = }')

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

        # GameOver flag
        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Start timing how long this takes -------------------------------------
        # draw_start_time = timeit.default_timer()
        # ----------------------------------------------------------------------

        # Wallpaper
        arcade.draw_lrwh_rectangle_textured(
            self.view_left,
            self.view_bottom,
            self.screen_width,
            self.screen_height,
            self.background,
            # alpha=180,
        )

        # Draw game items
        self.wall_list.draw()
        self.floor_list.draw()
        self.items_list.draw()
        self.player_list.draw()
        self.exit_list.draw()

        # Show minimap
        if self.show_minimap:
            self.generate_minimap()

        # ItemBar panel #1
        arcade.draw_rectangle_filled(
            center_x=self.view_left + 48,
            center_y=self.screen_height - 20 + self.view_bottom,
            width=90,
            height=33,
            color=(0, 96, 96, 180)
            # (250, 80, 0, 200)
        )

        # Collect items
        self.items_bar_battery.set_position(
            center_x=self.view_left + 20,
            center_y=self.screen_height - 20 + self.view_bottom,
        )
        self.items_bar_battery.draw()
        # Score
        output = f'{self.score} / {self.of_score}'
        arcade.draw_text(output,
                         self.view_left + 40,
                         self.screen_height - 32.5 + self.view_bottom,
                         arcade.color.WHITE, 16)

        # Draw game over
        if self.game_over:
            x = self.view_left + (self.screen_width / 2) - 200
            y = self.screen_height - (self.screen_height / 2) + self.view_bottom
            arcade.draw_text('Game Over', x, y, arcade.color.RED_DEVIL, 90, bold=True)

        # print(f'{self.view_left = }')
        # print(f'{self.view_bottom = }')

        # self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        start_time = timeit.default_timer()

        if not self.game_over:
            self.physics_engine.update()

            # Update the players animation
            self.player_list.update_animation()

            # Battery items animation
            self.items_list.update_animation()

            # for DEMO
            # self.exit_list.update_animation()

        # Update Item exit level animation depending on the number of scores
        if self.score < self.of_score:
            self.exit_sprite.texture = self.exit_sprite.idle_texture
        else:
            self.exit_list.update_animation()
            exit_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.exit_list)

            for _ in exit_hit_list:
                self.player_sprite.teleport()
                # self.player_sprite.kill()
                self.game_over = True

        # Collisions with items
        battery_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.items_list)

        for item in battery_hit_list:
            item.kill()
            self.score += 1

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

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
            # self.show_full_map()
            self.show_minimap = True

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
            # self.show_full_map(release=True)
            self.show_minimap = False
            self.minimap_list = None

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

        print(f'{x=} {y=}')

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
            # ratio = (self.sprite_size * self.maze_width) / self.screen_width
            ratio = (self.sprite_size * self.maze_height) / self.screen_height
            print('1 cond')
        elif self.screen_height < self.screen_width and self.maze_width < self.maze_height:
            ratio = (self.sprite_size * self.maze_height) / self.screen_height
            print('2 cond')
        elif self.screen_height < self.screen_width and self.maze_width == self.maze_height:
            ratio = (self.sprite_size * self.maze_width) / self.screen_height
            # ratio = (self.sprite_size * self.maze_height) / self.screen_width
            print('3 cond')

        elif self.screen_height > self.screen_width and self.maze_height > self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_height
            print('4 cond')
        elif self.screen_height > self.screen_width and self.maze_height < self.maze_width:
            ratio = (self.sprite_size * self.maze_width) / self.screen_width
            print('5 cond')
        elif self.screen_height > self.screen_width and self.maze_height == self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            print('6 cond')

        elif self.screen_height == self.screen_width and self.maze_height > self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            print('7 cond')
        elif self.screen_height == self.screen_width and self.maze_height < self.maze_width:
            ratio = (self.sprite_size * self.maze_width) / self.screen_height
            print('8 cond')
        elif self.screen_height == self.screen_width and self.maze_height == self.maze_width:
            ratio = (self.sprite_size * self.maze_height) / self.screen_width
            print('9 cond')

        print(f'{ratio = }')

        return ratio

    def generate_minimap(self) -> None:
        """
        Generating a static minimap and other game items using a one-pixel sprite

        :return: None
        """

        # Check list
        self.minimap_list = arcade.SpriteList()

        # List unused coordinates in minimap
        # unused_coords = []

        # Generating a minimap using a one-pixel sprite
        for row in range(self.maze_height):
            for column in range(self.maze_width):
                # Walls
                if self.maze[row][column] == 1:
                    self.minimap = arcade.Sprite(self.minimap_sprite, self.minimap_sprite_scaling)

                    x = column * self.minimap_sprite_size + self.minimap_sprite_size / 2
                    y = row * self.minimap_sprite_size + self.minimap_sprite_size / 2

                    # Set the position based on the current camera position
                    self.minimap.center_x = x + self.view_left + (self.screen_width - self.minimap_width) - 5
                    self.minimap.center_y = y + self.view_bottom + 5
                    self.minimap_list.append(self.minimap)

                # Empty (floor) coords
                # else:
                #     unused_coords.append((
                #         (column * self.minimap_sprite_size + self.minimap_sprite_size / 2) +
                #         self.view_left + (self.screen_width - self.minimap_width) - 5,
                #
                #         (row * self.minimap_sprite_size + self.minimap_sprite_size / 2 + self.view_bottom + 5)
                #     ))

        # Mark exit
        # minimap_exit_coords_idx = unused_coords.index(min([i for i in unused_coords]))
        # minimap_exit_start_coords = unused_coords.pop(minimap_exit_coords_idx)
        # print(f'{minimap_exit_start_coords = }')
        # self.minimap_exit_sprite.set_position(
        #     center_x=minimap_exit_start_coords[0],
        #     center_y=minimap_exit_start_coords[1],
        # )


        minimap_exit_x = (self.minimap_sprite_size + self.minimap_sprite_size / 2) + self.view_left + (self.screen_width - self.maze_width) - 5 - self.exit_start_coords[0] + self.minimap_width - self.minimap_sprite_size - self.sprite_size
        minimap_exit_y = (self.minimap_sprite_size + self.minimap_sprite_size / 2) + self.view_bottom + 5
        # print(f'{minimap_exit_x = }')
        # print(f'{minimap_exit_y = }')

        self.minimap_exit_sprite.set_position(
            center_x=minimap_exit_x,
            center_y=minimap_exit_y,
        )

        # Generate Items
        for item in self.battery_coords_list:
            x, y = item
            battery = self.minimap_item_sprite
            battery.center_x = (self.minimap_sprite_size + self.minimap_sprite_size / 2) + self.view_left + (self.screen_width - self.maze_width) - 5 - x + (self.maze_width * self.minimap_sprite_size) - self.minimap_sprite_size - self.sprite_size
            battery.center_y = (self.minimap_sprite_size + self.minimap_sprite_size / 2) + self.view_bottom + 5
            self.minimap_items_list.append(battery)

        # Draw minimap background
        arcade.draw_rectangle_filled(
            width=self.minimap_width,
            height=self.minimap_height,
            center_x=self.minimap_x + self.view_left,    # 220,
            center_y=self.minimap_y + self.view_bottom,  # 430,
            # color=(0, 250, 0, 255),
            color=(0, 0, 0, 180),
        )

        # Draw minimap
        self.minimap_list.draw()
        self.minimap_exit_sprite.draw()
        self.minimap_items_list.draw()
