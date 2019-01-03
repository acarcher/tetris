from curses import wrapper

from ex45_engine import Engine
from ex45_board import Board

# FIXME 1: The game_window scrolls up by one line or fails when height is not
# + 1 greater than area being written to, also forces border window to be
# 1 unit longer in y; not initially a problem and unknown cause

# TODO 1: Spawn pieces above play area
#   * 2-4 invisible rows (vanish zone) https://harddrop.com/wiki/Playfield
#   * allows other types of losses

# TODO 2: Wall-kicking

# TODO 3: Soft dropping and hard dropping

# TODO 4: Find what the default background color is when wrapper inits
# and how that interacts with the curses.use_default_colors() call, in an
# attempt to make the program display similarly regardless of terminal

# TODO 5: Better debugging
#   * separate debugger that has access to windows and handles curses directly

# TODO 6: Document, rename, reorder, PEP8-ify


def main(screen):
    board = Board(screen, debug=False)
    game = Engine(board, 1)
    game.run()


if __name__ == "__main__":
    wrapper(main)
