import arcade

from grid_generator import make_maze  # noqa


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.screen_width = width
        self.screen_height = height

        self.maze_width = 51
        self.maze_height = 51

        self.native_sprite_size = 1  # 4
        self.sprite_scaling = 7      # 1.5
        self.sprite_size = self.native_sprite_size * self.sprite_scaling
        print(f'{self.sprite_size = }')

        self.minimap_width = self.sprite_size * self.maze_width    # 400
        print(f'{self.minimap_width = }')
        self.minimap_height = self.sprite_size * self.maze_height  # 300
        print(f'{self.minimap_height = }')
        self.minimap_x = self.screen_width - self.minimap_width / 2 - 5  # 220
        print(f'{self.minimap_x = }')
        self.minimap_y = self.minimap_height / 2 + 5
        print(f'{self.minimap_y = }')

        self.sprite_wall = r'teal_square.png'
        self.wall_list = None

        self.wall_lines_list = []

        self.show_minimap = False

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):

        self.wall_list = arcade.SpriteList()

        # Create the maze
        maze = make_maze(self.maze_width, self.maze_height)

        # Generate walls and floor
        for row in range(self.maze_height):
            for column in range(self.maze_width):
                if maze[row][column] == 1:
                    wall = arcade.Sprite(self.sprite_wall, self.sprite_scaling)

                    # self.wall_lines_list.append((column * 25 / 2, row * 25 / 2))
                    # self.wall_lines_list.append((column * 20 / 2, row + 580 / 2))

                    # x = (column + 20) * self.sprite_size + self.sprite_size / 2
                    # y = (row + 580) * self.sprite_size + self.sprite_size / 2
                    # x=895 y=700
                    # x = self.minimap_x / 2 + (column * self.sprite_size + self.sprite_size / 2)
                    x = self.minimap_x + (self.minimap_width / 2) - (column * self.sprite_size + self.sprite_size / 2)
                    y = self.minimap_y * 2 - (row * self.sprite_size + self.sprite_size / 2) - 5
                    # print(f'{x = } / {y = }')
                    self.wall_lines_list.append((x, y),)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                # else:
                #     # Add unused coords for place mics items
                #     self.unused_coords_list.append((
                #         column * self.sprite_size + self.sprite_size / 2,
                #         row * self.sprite_size + self.sprite_size / 2
                #     ))
                #
                #     # floor = arcade.Sprite(self.sprite_floor, self.sprite_scaling)
                #     floor = arcade.Sprite(random.choice(self.sprite_floor_list), self.sprite_scaling)
                #     floor.center_x = column * self.sprite_size + self.sprite_size / 2
                #     floor.center_y = row * self.sprite_size + self.sprite_size / 2
                #     self.floor_list.append(floor)

        # print()
        # [print(i) for i in maze]
        # [print(i) for i in self.wall_lines_list]
        # [print(i, i.set_position(i.position[0] - idx, i.position[1] - idx)) for idx, i in enumerate(self.wall_list)]

        pass

    def on_draw(self):
        arcade.start_render()

        if self.show_minimap:
            arcade.draw_rectangle_filled(
                width=self.minimap_width,
                height=self.minimap_height,
                center_x=self.minimap_x,  # 220,
                center_y=self.minimap_y,  # 430,
                color=(0, 0, 0, 255),
            )

            self.wall_list.draw()

    def on_key_press(self, key, key_modifiers):

        if key == arcade.key.M:
            self.show_minimap = True

    def on_key_release(self, key, key_modifiers):
        """
        Called when a user releases a mouse button.
        """

        if key == arcade.key.M:
            self.show_minimap = False

        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        # print(f'{x=} {y=}')

        pass


def main():
    window = MyGame(1200, 700, 'Starting Template Simple')
    window.setup()
    # print(window.get_viewport())
    arcade.run()


if __name__ == "__main__":
    main()
