# Handles displaying the board to screen

import curses
from tetris.config import CHAR
from tetris.piece import Piece


class Display(object):

    curses_colors_map = {
        "cyan": curses.COLOR_CYAN,
        "blue": curses.COLOR_BLUE,
        "white": curses.COLOR_WHITE,
        "yellow": curses.COLOR_YELLOW,
        "green": curses.COLOR_GREEN,
        "magenta": curses.COLOR_MAGENTA,
        "red": curses.COLOR_RED,
        "default": -1
    }

    def __init__(self, screen, height, width, debug=False):
        self.screen = screen
        self.height = height
        self.width = width
        self.debug = debug

        self.border_window = None
        self.game_window = None
        self.info_window = None
        self.debug_window = None

        self._init_curses()

    def _init_curses(self):

        curses.curs_set(False)

        dimensions = self.screen.getmaxyx()

        y_start = 0

        if self.debug:
            x_start = 0
        else:
            x_start = dimensions[1] // 2 - (self.width + 2) // 2

        self.border_window = curses.newwin(self.height + 3, self.width + 2,
                                           y_start, x_start)
        self.border_window.border()
        self.border_window.refresh()

        self.game_window = curses.newwin(self.height + 1, self.width,
                                         y_start + 1, x_start + 1)
        self.game_window.keypad(True)
        self.game_window.nodelay(True)

        # FIXME 1: self.game_window.scrollok(True)

        self.info_window = curses.newwin(self.height, self.width,
                                         0, x_start + self.width + 2)

        if self.debug:
            self.debug_window = curses.newwin(self.height, 45,
                                              0, x_start + self.width * 2 + 2)
        # TODO 4: curses.use_default_colors()

        curses.init_pair(curses.COLOR_CYAN,
                         curses.COLOR_CYAN,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_BLUE,
                         curses.COLOR_BLUE,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_WHITE,
                         curses.COLOR_WHITE,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_YELLOW,
                         curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_GREEN,
                         curses.COLOR_GREEN,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_MAGENTA,
                         curses.COLOR_MAGENTA,
                         curses.COLOR_BLACK)

        curses.init_pair(curses.COLOR_RED,
                         curses.COLOR_RED,
                         curses.COLOR_BLACK)

        # TODO 4: Own attempt at creating a default
        #
        # curses.init_pair(COLOR_DEFAULT,
        #                  curses.COLOR_WHITE,
        #                  curses.COLOR_BLACK)

        # TODO 4: Default supplied by terminal
        # curses.init_pair(COLOR_DEFAULT,
        #                  -1,
        #                  -1)

    # get user input and only one input per tick
    def get_input(self):

        char = self.game_window.getch()
        curses.flushinp()
        return char

    # write the board to the terminal
    def draw_board(self, board_state):

        for y_idx, row in enumerate(board_state):
            for x_idx, col in enumerate(row):

                char = board_state[y_idx][x_idx]
                color = self._get_piece_color(char)

                if color:
                    self.game_window.addstr(y_idx, x_idx, CHAR,
                                            curses.color_pair(color))
                else:
                    self.game_window.addstr(y_idx, x_idx, char)

        self.game_window.refresh()

    def _get_piece_color(self, symbol):

        if symbol in ("@", "#", "$", "%", "&", "+", "="):
            color_name = Piece.symbol_to_color[symbol]
        else:
            # TODO 4: color_name = Piece.symbol_to_color["default"]
            return None

        return self.curses_colors_map[color_name]

    def draw_score(self, score):

        self.info_window.addstr(1, 0, "Score:")
        self.info_window.addstr(2, 0, " " * self.width)
        self.info_window.addstr(2, 0, str(score))
        self.info_window.refresh()

    def draw_next_piece(self, next_piece):

        self.info_window.addstr(7, 0, "Next:")
        first, second, third, fourth = next_piece._get_default_location(8, self.width)

        self.info_window.addstr(8, 0, " " * self.width)
        self.info_window.addstr(9, 0, " " * self.width)

        color = self._get_piece_color(next_piece.symbol)

        self.info_window.addstr(first[0], first[1], CHAR,
                                curses.color_pair(color))
        self.info_window.addstr(second[0], second[1], CHAR,
                                curses.color_pair(color))
        self.info_window.addstr(third[0], third[1], CHAR,
                                curses.color_pair(color))
        self.info_window.addstr(fourth[0], fourth[1], CHAR,
                                curses.color_pair(color))

        self.info_window.refresh()

    def draw_level(self, level):

        self.info_window.addstr(4, 0, "Level:")
        self.info_window.addstr(5, 0, " " * self.width)
        self.info_window.addstr(5, 0, str(level))
        self.info_window.refresh()

    def draw_game_over(self):

        for y in range(0, self.height):
            for x in range(0, self.width):
                self.game_window.addstr(y, x, " ")

        start_height = (self.height - 1) // 2
        start_width = self.width // 2

        self.game_window.addstr(start_height, start_width - (len("Game over") + 1) // 2,
                                "Game over")
        self.game_window.addstr(start_height + 2, start_width - (len("Continue?") + 1) // 2,
                                "Continue?")
        self.game_window.addstr(start_height + 3, start_width - (len("y/n") + 1) // 2,
                                "y/n")
