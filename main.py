from curses import wrapper

from engine import Engine
from board import Board
from display import Display
from config import SPEED, DEBUG, TICK_LENGTH, HEIGHT, WIDTH

# FIXME 1: The game_window scrolls up by one line or fails when height is not
# + 1 greater than area being written to, also forces border window to be
# 1 unit longer in y; not initially a problem and unknown cause

# TODO 1: Spawn pieces above play area
#   * 2-4 invisible rows (vanish zone) https://harddrop.com/wiki/Playfield
#   * allows other types of losses

# TODO 2: Wall-kicking

# TODO 3: Soft dropping and hard dropping

# TODO 4: Find what the default background color is when wrapper inits
# and how that interacts with the curses.use_default_colors() call, for proper
# cross-platform, cross-terminal display

# TODO 5: Better debugging
#   * separate debugger/logger that has access to windows and handles curses directly

# TODO 6: Document

# TODO 7: Make force dropping increase score

# TODO 8: Add counter-clockwise rotation

# TODO 9: Add generic rotation algorithm

# Curses references:
# https://docs.python.org/3.6/library/curses.html
# https://docs.python.org/3/howto/curses.html


# TODO: Ideally debug is passed into engine
# TODO: Remove display from being passed to board
def main(screen):

    display = Display(screen, HEIGHT, WIDTH, debug=DEBUG)
    board = Board(display, HEIGHT, WIDTH, debug=DEBUG)
    game = Engine(board, display, SPEED, TICK_LENGTH)
    game.run()


if __name__ == "__main__":

    wrapper(main)
