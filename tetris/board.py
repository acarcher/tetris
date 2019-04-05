# Display and controls
# A board takes input

import curses
import random

from tetris.piece import Piece

# TODO 4: # COLOR_DEFAULT = 8


class Board(object):

    # TODO: remove display
    def __init__(self, display, height, width, vanish_zone=0, debug=False):

        if height % 2 != 0:
            raise ValueError("Height must be even")
        if width % 2 != 0:
            raise ValueError("Width must be even")
        if height / 2 != width:
            raise ValueError("Width must be half of height")
        self.display = display
        self.height = height
        self.width = width
        self.vanish_zone = vanish_zone
        self.debug = debug

        self.board_state = self._init_board_state()
        self.current_piece = self.generate_rand_piece()
        self.next_piece = self.generate_rand_piece()

    # Physical representation of the board and borders
    def _init_board_state(self):

        return [["." for x in range(0, self.width)]
                for y in range(0, self.height + self.vanish_zone)]

    # get the next piece
    def generate_rand_piece(self):

        if self.debug:
            return Piece("I")

        return [Piece("I"), Piece("J"), Piece("L"), Piece("O"),
                Piece("S"), Piece("T"), Piece("Z")][random.randint(0, 6)]

    def reset_board_state(self):

        self.board_state = self._init_board_state()

    def check_and_update(self, action, next_pos):

        if not self._is_invalid_move(next_pos):  # validity check and update
            if self.debug:
                self.display.debug_window.addstr(11, 0, "valid move")
                self.display.debug_window.refresh()

            self._update_piece_position(action, next_pos)

        # Check for collisions and OOB
    def _is_invalid_move(self, next_pos):

        if self.debug:
            out_of_bounds = False
            collision = False

            self.display.debug_window.addstr(6, 0, "next_pos: {}       ".format(next_pos))
            self.display.debug_window.refresh()

            out_of_bounds = self._is_oob(next_pos)

            self.display.debug_window.addstr(4, 0, "out_of_bounds: {} ".format(out_of_bounds))
            self.display.debug_window.refresh()

            if out_of_bounds:
                return out_of_bounds

            collision = self._is_collision(next_pos)

            self.display.debug_window.addstr(5, 0, "collision: {}".format(collision))
            self.display.debug_window.refresh()

            return out_of_bounds or collision

        return self._is_oob(next_pos) or self._is_collision(next_pos)

    def _is_oob(self, next_pos):

        # Out of bounds check
        for point in next_pos:
            if point[0] < 0 or point[0] > self.height - 1:
                if self.debug:
                    self.display.debug_window.addstr(8, 0, "height <0: {}".format(point[0] < 0))
                    self.display.debug_window.addstr(9, 0, "height >: {}".format(point[0] > self.height - 1))
                    self.display.debug_window.refresh()
                return True
            elif point[1] < 0 or point[1] > self.width - 1:
                if self.debug:
                    self.display.debug_window.addstr(10, 0, "width <0: {}".format(point[1] < 0))
                    self.display.debug_window.addstr(11, 0, "width >: {}".format(point[1] > self.width - 1))
                    self.display.debug_window.refresh()
                return True
        if self.debug:
            self.display.debug_window.addstr(8, 0, " " * 20)
            self.display.debug_window.addstr(9, 0, " " * 20)
            self.display.debug_window.addstr(10, 0, " " * 20)
            self.display.debug_window.addstr(11, 0, " " * 20)
            self.display.debug_window.refresh()
        return False

    # when in contact with another piece
    def _is_collision(self, next_pos):
        # Collision check from below
        for point in next_pos:
            if (point not in self.current_piece.location
               and self.board_state[point[0]][point[1]] != "."):

                return True
        return False

    # Update board representation and piece location
    def _update_piece_position(self, action, next_pos):

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = "."

        self.current_piece.location = next_pos

        if action == curses.KEY_UP:
            self.current_piece.orientation = (self.current_piece.orientation + 1) % 4

        for point in self.current_piece.location:
            self.board_state[point[0]][point[1]] = self.current_piece.symbol

    # Check for a complete row
    def check_rows(self):
        full_rows = []

        for i, row in enumerate(self.board_state):
            if "." not in row:
                full_rows.append(i)

        return full_rows

    # Move rows down after clears
    # Credit: Michael Stikkel
    def clear_and_move_rows(self):

        row = self.height - 1
        count = 0

        while row > 0:
            if self.debug:
                count += 1
                self.display.debug_window.addstr(10, 0, "row: {} ".format(row))
                self.display.debug_window.addstr(11, 0, "count: {} ".format(count))
                self.display.debug_window.refresh()

            if self._is_full(self.board_state[row]):
                self.board_state[0:row + 1] = [["."] * self.width] + self.board_state[0:row]
            else:
                row -= 1

    # Credit: Michael Stikkel
    def _is_full(self, row):

        return all(v != "." for v in row)

    # http://tetris.wikia.com/wiki/Top_out
    def is_loss(self, piece):

        default_position = piece._get_default_location(0, self.width)

        if self._is_block_out(default_position):
            return True
        elif self._is_lock_out():
            return True
        else:
            return False

    # Determine if default blocks are occupied
    def _is_block_out(self, default_position=[]):

        for point in default_position:
            if self.board_state[point[0]][point[1]] != ".":
                return True

        return False

    # TODO 1: if no points inside the playable area
    def _is_lock_out(self):

        for point in self.current_piece.location:
            pass

    # Start the next piece
    def add_new_piece(self, piece):

        default_location = self.next_piece._get_default_location(0, self.width)

        self.current_piece = self.next_piece
        self.current_piece.location = default_location

        self._add_piece_to_board(self.current_piece)

        self.next_piece = piece

    def _add_piece_to_board(self, piece):

        for point in piece.location:
            self.board_state[point[0]][point[1]] = piece.symbol

    # Default piece movement
    def apply_gravity(self):

        return self.current_piece.move(curses.KEY_DOWN)

    # Determine if piece landed
    def check_piece_landed(self):

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

