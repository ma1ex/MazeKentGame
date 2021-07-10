from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(width=1200, height=700, title='MazeKent')
    game.maze_width = 21 # 25
    game.maze_height = 21 # 14
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
