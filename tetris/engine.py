# Driver and state transitions
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from sys import exit


class Engine(object):

    # board: board to play
    # speed: how many seconds per action (period)
    # score: points earned
    # tick_length: period of the game

    def __init__(self, board, display, speed, tick_length):

        if speed < 0:
            raise ValueError("Speed cannot be negative")

        self.board = board
        self.display = display
        self.speed = speed
        self.tick_length = tick_length
        self.max_level = speed // tick_length

        self.speed_mod = 0
        self.tick = 0
        self.score = 0
        self.level = 0
        self.rows_cleared = 0
        self.game_over = False

    def run(self):

        try:
            while(True):
                self._loop_game_logic()
                self._handle_game_over()

        except KeyboardInterrupt:
            self._exit_game()

    def _loop_game_logic(self):

        self.board.add_new_piece(self.board.generate_rand_piece())

        while(not self.game_over):
            if self.display.debug:
                self.display.debug_window.addstr(0, 0, "Tick: {}".format(self.tick))
                self.display.debug_window.refresh()

            self.display.draw_board(self.board.board_state)
            self.display.draw_score(self.score)
            self.display.draw_level(self.level)
            self.display.draw_next_piece(self.board.next_piece)

            key_pressed = self.display.get_input()

            if self.display.debug:
                self.display.debug_window.addstr(1, 0, "Key pressed: {} ".format(key_pressed))
                self.display.debug_window.refresh()

            if key_pressed in (KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, ord('q')):

                self.board.check_and_update(*self._dispatch_action(key_pressed))

                if self.board.check_piece_landed():
                    self._handle_piece_landed()
                    self.display.draw_next_piece(self.board.next_piece)

            if self.tick % ((self.speed - self.speed_mod)
               // self.tick_length + 1) == 0:  # default movement

                self.board.check_and_update(None, self.board.apply_gravity())
                if self.display.debug:
                    self.display.debug_window.addstr(2, 0, "Gravity: {}".format(self.tick))
                    self.display.debug_window.addstr(3, 0, "New piece: {}".format(False))
                    self.display.debug_window.refresh()

                if self.board.check_piece_landed():
                    self._handle_piece_landed()

            # https://stackoverflow.com/a/25251804
            time.sleep(self.tick_length - time.time() % self.tick_length)
            self.tick += 1

    # Takes in key_press, returns the correct action
    def _dispatch_action(self, key_press):

        move_keys = (KEY_RIGHT, KEY_LEFT, KEY_DOWN)

        rotate_key = (KEY_UP,)

        if key_press == ord('q'):
            self.exit_game()
        elif key_press in move_keys:
            return key_press, self.board.current_piece.move(key_press)
        elif key_press in rotate_key:
            return key_press, self.board.current_piece.rotate_clockwise()
        else:
            raise ValueError("Key not bound")

    def _exit_game(self):
        exit(0)

    def _handle_piece_landed(self):

        if self.board.is_loss(self.board.current_piece):  # check for lock or block
            self.game_over = True
            return
        else:
            full_rows = self.board.check_rows()

            if full_rows:
                self._update_state(full_rows)
                self.display.draw_score(self.score)
                self.display.draw_level(self.level)
                self.board.clear_and_move_rows()

            if self.display.debug:
                self.display.debug_window.addstr(3, 0, "New piece: {} ".format(True))

            self._handle_new_piece()

    def _update_state(self, full_rows):

        self.rows_cleared += len(full_rows)
        self.level = self._calculate_level()
        self.speed_mod = self.level * self.tick_length
        self.score += self._calculate_score(full_rows)

    def _calculate_level(self):
        return self.rows_cleared // 5 if self.rows_cleared // 5 < self.max_level else self.max_level

    # https://tetris.wiki/Scoring
    # Nintendo scoring
    def _calculate_score(self, full_rows):

        lines_cleared = len(full_rows)
        line_mult = [40, 100, 300, 1200]

        score = line_mult[lines_cleared - 1] * (self.level + 1)

        return score

    # new piece loop
    def _handle_new_piece(self):

        next_piece = self.board.generate_rand_piece()

        if self.board.is_loss(next_piece):
            self.game_over = True
            return
        else:
            self.board.add_new_piece(next_piece)

    def _handle_game_over(self):

        self.display.draw_game_over()

        self.display.game_window.nodelay(False)

        while(self.game_over):
            key = self.display.get_input()

            if key == ord('y'):
                self.display.game_window.nodelay(True)
                self._reset_engine_state()
                self.board.reset_board_state()
            elif key == ord('n'):
                self.display.game_window.nodelay(True)
                self._exit_game()
            else:
                continue

    def _reset_engine_state(self):

        self.rows_cleared = 0
        self.level = 0
        self.speed_mod = 0
        self.score = 0
        self.tick = 0
        self.game_over = False