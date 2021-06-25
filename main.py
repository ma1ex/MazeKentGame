from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(width=1200, height=720, title='MazeKent')
    game.maze_width = 11 # 25
    game.maze_height = 11 # 14
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
