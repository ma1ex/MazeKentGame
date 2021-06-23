from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(width=1280, height=720, title='MazeKent')
    game.maze_width = 20
    game.maze_height = 20
    game.setup()
    # game.run()


if __name__ == '__main__':
    main()
