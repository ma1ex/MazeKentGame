from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(width=720, height=720, title='MazeKent')
    game.maze_width = 41 # 25
    game.maze_height = 41 # 14
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
