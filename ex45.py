import curses
from ex45_engine import Engine
from ex45_board import Board

# TODO
# spawn pieces above play area
#   2-4 invisible rows (vanish zone) https://harddrop.com/wiki/Playfield
#   allows other types of losses
# wall-kicking
# soft dropping and hard dropping


def main(screen):
    board = Board(screen, debug=False)
    game = Engine(board, 1)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)
