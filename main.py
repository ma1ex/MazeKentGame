import arcade
from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(width=800, height=800, title='MazeKent')
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
