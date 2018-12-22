# Display and controls
# A board takes input
import curses
import time

from ex45_piece import Piece


class Board(object):

    terminal_colors = {
        "cyan": "\033[36m",
        "blue": "\033[34m",
        "white": "\033[37m",
        "yellow": "\033[33m",
        "green": "\033[32m",
        "magenta": "\033[35m",
        "red": "\033[31m",
        "reset": "\033[0m"
    }

    curses_colors = {
        "cyan": curses.COLOR_CYAN,
        "blue": curses.COLOR_BLUE,
        "white": curses.COLOR_WHITE,
        "yellow": curses.COLOR_YELLOW,
        "green": curses.COLOR_GREEN,
        "magenta": curses.COLOR_MAGENTA,
        "red": curses.COLOR_RED
    }

    def __init__(self, screen, height=20, width=10, vanish_zone=0, debug=False):
        assert(height % 2 == 0)
        assert(width % 2 == 0)
        assert(height / 2 == width)
        self.height = height
        self.width = width
        self.board_state = self.create_state(height, width, vanish_zone)
        self.screen = screen
        self.border_window = None
        self.game_window = None
        self.score_window = None
        self.debug_window = None
        self.current_piece = None
        self.debug = debug

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

        # FIXME: The game_window scrolls up by one line or fails when height is not
        # + 1 greater than area being written to, also forces border window to be
        # larger; not initially a problem and unknown cause
        # self.game_window.scrollok(True)

        self.score_window = curses.newwin(self.height, self.width,
                                          0, x_start + self.width + 2)

        if self.debug:
            self.debug_window = curses.newwin(self.height, 45,
                                              0, x_start + self.width * 2 + 2)

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

    # Physical representation of the board and borders
    def create_state(self, height, width, vanish):
        return [["." for x in range(0, width)]
                for y in range(0, height + vanish)]

    # write the board to the terminal
    # FIXME
    def draw(self):
        attributes = Piece.tetromino_attributes.values()

        for y_idx, row in enumerate(self.board_state):
            for x_idx, col in enumerate(row):
                char = self.board_state[y_idx][x_idx]

                # TODO: improve this logic so it it doesn't do 6 scans per char
                for attr in attributes:
                    if char == attr[1]:
                        color = self.curses_colors[attr[0]]
                        break
                    else:
                        color = None

                if color:
                    self.game_window.addstr(y_idx, x_idx, b'\xe2\x96\xa0',
                                            curses.color_pair(color))
                else:
                    self.game_window.addstr(y_idx, x_idx, char)

        self.game_window.refresh()

    # get user input and only one input per tick
    def get_input(self):
        char = self.game_window.getch()
        curses.flushinp()
        return char

    # Default location for each piece
    # http://tetris.wikia.com/wiki/SRS
    def get_default_location(self, piece):
        tetrimino = piece.tetromino
        x_cl = self.width // 2  # center left
        y = 1

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
            raise Exception("Incorrect tetrimino")

    # get the next piece
    def random_piece(self, random_int):
        return [Piece("I"), Piece("J"), Piece("L"), Piece("O"),
                Piece("S"), Piece("T"), Piece("Z")][random_int]

    # Default piece movement
    def gravity(self):
        return self.current_piece.move(curses.KEY_DOWN)

    # Check for collisions and OOB
    def invalid_move(self, next_pos):
        out_of_bounds = False
        collision = False

        if self.debug:
            self.debug_window.addstr(6, 0, "next_pos: {}       ".format(next_pos))
            self.debug_window.refresh()

            out_of_bounds = self.is_oob(next_pos)

            self.debug_window.addstr(4, 0, "out_of_bounds: {} ".format(out_of_bounds))
            self.debug_window.refresh()

            # Avoids going to is_collision index out of range
            # TODO: make this better
            # When I don't need printing..
            # can just return the functions in correct order
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
                    self.debug_window.addstr(7, 0, "height <0: {}".format(point[0] < 0))
                    self.debug_window.addstr(8, 0, "height >: {}".format(point[0] > self.height - 1))
                    self.debug_window.refresh()
                return True
            elif point[1] < 0 or point[1] > self.width - 1:
                if self.debug:
                    self.debug_window.addstr(9, 0, "width <0: {}".format(point[1] < 0))
                    self.debug_window.addstr(10, 0, "width >: {}".format(point[1] > self.width - 1))
                    self.debug_window.refresh()
                return True
        if self.debug:
            self.debug_window.addstr(7, 0, " " * 20)
            self.debug_window.addstr(8, 0, " " * 20)
            self.debug_window.addstr(9, 0, " " * 20)
            self.debug_window.addstr(10, 0, " " * 20)
            self.debug_window.refresh()
        return False

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
    def update_piece_position(self, next_pos):

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = "."

        self.current_piece.location = next_pos

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = self.current_piece.symbol

    # Clear complete rows
    # FIXME: off by one error when multiple lines cleared
    def clear_full_rows(self, full_rows):
        accumulated_rows = 0

        for full_row in full_rows:
            self.board_state[full_row][:] = ["."] * len(self.board_state[full_row][:])

        for row_num, row in zip(reversed(range(self.height)),
                                self.board_state[::-1]):

            if row_num in full_rows:
                accumulated_rows += 1

            if row_num - accumulated_rows < 0:
                self.board_state[row_num][:] = self.board_state[0][:]
                pass
            else:
                self.board_state[row_num][:] = self.board_state[row_num - accumulated_rows][:]

        # clear all full rows
        # work from bottom to top figuring out how many lines to
        # move each piece by number of accumulated empty rows

    # Start the next piece
    def add_new_piece(self, piece):

        default_location = self.get_default_location(piece)

        self.current_piece = piece
        self.current_piece.location = default_location

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = self.current_piece.symbol

    # if the next position downward of any block is anything other
    # than nothing or itself

    # if it's at the bounds
    # if it's touching another piece
    # TODO: validate
    def piece_landed(self):

        for point in self.current_piece.location:
            if point[0] == self.height - 1:
                return True

            downward = [point[0] + 1, point[1]]

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

    def _lock_out(self):
        for point in self.current_piece.location:
            pass
            # if no points inside the playable area TODO

    # http://tetris.wikia.com/wiki/Top_out
    def is_loss(self, piece):
        default_position = self.get_default_location(piece)

        if self._block_out(default_position):
            return True
        elif self._lock_out():
            return True
        else:
            return False

    # TODO
    def game_over(self):
        pass
