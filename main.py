from mazekent_game import MazeKent


def main():
    
    print('> Starting game...\n')

    game = MazeKent(
        title='MazeKent',
        width=1200,
        height=700,
        maze_width=11,  # 25
        maze_height=11  # 14
    )
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
