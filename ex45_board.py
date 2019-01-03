# Display and controls
# A board takes input

import curses
import random

from ex45_piece import Piece, CHAR

# TODO 4: # COLOR_DEFAULT = 8


class Board(object):

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

    def __init__(self, screen, height=20, width=10, vanish_zone=0, debug=False):

        if height % 2 != 0:
            raise ValueError("Height must be even")
        if width % 2 != 0:
            raise ValueError("Width must be even")
        if height / 2 != width:
            raise ValueError("Width must be half of height")

        self.screen = screen

        self.height = height
        self.width = width
        self.vanish_zone = vanish_zone
        self.debug = debug

        self.board_state = self.init_board_state()
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()

        self.border_window = None
        self.game_window = None
        self.info_window = None
        self.debug_window = None

        self.init_curses()

    def init_curses(self):

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

    # Physical representation of the board and borders
    def init_board_state(self):
        return [["." for x in range(0, self.width)]
                for y in range(0, self.height + self.vanish_zone)]

    def reset_board_state(self):
        self.board_state = self.init_board_state()

    # write the board to the terminal
    def draw_board(self):
        for y_idx, row in enumerate(self.board_state):
            for x_idx, col in enumerate(row):

                char = self.board_state[y_idx][x_idx]
                color = self.get_piece_color(char)

                if color:
                    self.game_window.addstr(y_idx, x_idx, CHAR,
                                            curses.color_pair(color))
                else:
                    self.game_window.addstr(y_idx, x_idx, char)

        self.game_window.refresh()

    def get_piece_color(self, symbol):

        if symbol in ("@", "#", "$", "%", "&", "+", "="):
            color_name = Piece.symbol_to_color[symbol]
        else:
            # TODO 4: color_name = Piece.symbol_to_color["default"]
            return None

        return self.curses_colors_map[color_name]

    def draw_score(self, score):
        self.info_window.addstr(1, 0, "Score:")
        self.info_window.addstr(2, 0, str(score))
        self.info_window.refresh()

    def draw_next_piece(self):
        self.info_window.addstr(7, 0, "Next:")
        first, second, third, fourth = self.get_default_location(self.next_piece,
                                                                 8, self.width)

        self.info_window.addstr(8, 0, " " * self.width)
        self.info_window.addstr(9, 0, " " * self.width)

        color = self.get_piece_color(self.next_piece.symbol)

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

    # get user input and only one input per tick
    def get_input(self):
        char = self.game_window.getch()
        curses.flushinp()
        return char

    # Default location for each piece
    # http://tetris.wikia.com/wiki/SRS
    def get_default_location(self, piece, ref_pt_y, ref_pt_x):
        tetrimino = piece.tetromino
        y = ref_pt_y + 1
        x_cl = ref_pt_x // 2  # center left

        if tetrimino == "I":
            return [[y, x_cl - 2], [y, x_cl - 1],
                    [y, x_cl], [y, x_cl + 1]]
        elif tetrimino == "J":
            return [[y - 1, x_cl - 2], [y, x_cl - 2],
                    [y, x_cl - 1], [y, x_cl]]
        elif tetrimino == "L":
            return [[y - 1, x_cl], [y, x_cl - 2],
                    [y, x_cl - 1], [y, x_cl]]
        elif tetrimino == "O":
            return [[y - 1, x_cl - 1], [y - 1, x_cl],
                    [y, x_cl - 1], [y, x_cl]]
        elif tetrimino == "S":
            return [[y - 1, x_cl - 1], [y - 1, x_cl],
                    [y, x_cl - 2], [y, x_cl - 1]]
        elif tetrimino == "T":
            return [[y - 1, x_cl - 1], [y, x_cl - 2],
                    [y, x_cl - 1], [y, x_cl]]
        elif tetrimino == "Z":
            return [[y - 1, x_cl - 2], [y - 1, x_cl - 1],
                    [y, x_cl - 1], [y, x_cl]]
        else:
            raise ValueError("Incorrect tetrimino")

    # get the next piece
    def random_piece(self):
        if self.debug:
            return Piece("I")

        return [Piece("I"), Piece("J"), Piece("L"), Piece("O"),
                Piece("S"), Piece("T"), Piece("Z")][random.randint(0, 6)]

    # Default piece movement
    def gravity(self):
        return self.current_piece.move(curses.KEY_DOWN)

    # Check for collisions and OOB
    def invalid_move(self, next_pos):

        if self.debug:
            out_of_bounds = False
            collision = False

            self.debug_window.addstr(6, 0, "next_pos: {}       ".format(next_pos))
            self.debug_window.refresh()

            out_of_bounds = self.is_oob(next_pos)

            self.debug_window.addstr(4, 0, "out_of_bounds: {} ".format(out_of_bounds))
            self.debug_window.refresh()

            if out_of_bounds:
                return out_of_bounds

            collision = self.is_collision(next_pos)

            self.debug_window.addstr(5, 0, "collision: {}".format(collision))
            self.debug_window.refresh()

            return out_of_bounds or collision

        return self.is_oob(next_pos) or self.is_collision(next_pos)

    def is_oob(self, next_pos):

        # Out of bounds check
        for point in next_pos:
            if point[0] < 0 or point[0] > self.height - 1:
                if self.debug:
                    self.debug_window.addstr(8, 0, "height <0: {}".format(point[0] < 0))
                    self.debug_window.addstr(9, 0, "height >: {}".format(point[0] > self.height - 1))
                    self.debug_window.refresh()
                return True
            elif point[1] < 0 or point[1] > self.width - 1:
                if self.debug:
                    self.debug_window.addstr(10, 0, "width <0: {}".format(point[1] < 0))
                    self.debug_window.addstr(11, 0, "width >: {}".format(point[1] > self.width - 1))
                    self.debug_window.refresh()
                return True
        if self.debug:
            self.debug_window.addstr(8, 0, " " * 20)
            self.debug_window.addstr(9, 0, " " * 20)
            self.debug_window.addstr(10, 0, " " * 20)
            self.debug_window.addstr(11, 0, " " * 20)
            self.debug_window.refresh()
        return False

    # when in contact with another piece
    def is_collision(self, next_pos):
        # Collision check from below
        for point in next_pos:
            if (point not in self.current_piece.location
               and self.board_state[point[0]][point[1]] != "."):

                return True
        return False

    # Check for a complete row
    def check_rows(self):
        full_rows = []

        for i, row in enumerate(self.board_state):
            if "." not in row:
                full_rows.append(i)

        return full_rows

    # Update board representation and piece location
    def update_piece_position(self, action, next_pos):

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = "."

        self.current_piece.location = next_pos

        if action == curses.KEY_UP:
            self.current_piece.orientation = (self.current_piece.orientation + 1) % 4

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = self.current_piece.symbol

    def full(self, row):
        return all(v != "." for v in row)

    # Move rows down after clears
    # Credit: Michael Stikkel
    def clear_and_move_rows(self):

        row = self.height - 1
        count = 0

        while row > 0:
            if self.debug:
                count += 1
                self.debug_window.addstr(10, 0, "row: {} ".format(row))
                self.debug_window.addstr(11, 0, "count: {} ".format(count))
                self.debug_window.refresh()

            if self.full(self.board_state[row]):
                self.board_state[0:row + 1] = [["."] * self.width] + self.board_state[0:row]
            else:
                row -= 1

    # Start the next piece
    def add_new_piece(self, piece):

        default_location = self.get_default_location(self.next_piece,
                                                     0, self.width)
        self.current_piece = self.next_piece
        self.current_piece.location = default_location

        self.add_piece_to_board(self.current_piece)

        self.next_piece = piece

    def add_piece_to_board(self, piece):
        for point in piece.location:
            self.board_state[point[0]][point[1]] = piece.symbol

    # Determine if piece landed
    def piece_landed(self):

        for point in self.current_piece.location:
            # at the bottom boundary
            if point[0] == self.height - 1:
                return True

            downward = [point[0] + 1, point[1]]

            # piece exists below
            if (downward not in self.current_piece.location
               and self.board_state[downward[0]][downward[1]] != "."):

                return True

        return False

    # Determine if default blocks are occupied
    def _block_out(self, default_position=[]):
        for point in default_position:
            if self.board_state[point[0]][point[1]] is not ".":
                return True

        return False

    # TODO 1: if no points inside the playable area
    def _lock_out(self):
        for point in self.current_piece.location:
            pass

    # http://tetris.wikia.com/wiki/Top_out
    def is_loss(self, piece):
        default_position = self.get_default_location(piece, 0, self.width)

        if self._block_out(default_position):
            return True
        elif self._lock_out():
            return True
        else:
            return False
