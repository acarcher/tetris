# Driver and state transitions
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from sys import exit


class Engine(object):

    # board: board to play
    # speed: how many seconds per action (period)
    # score: points earned
    # tick_length: period of the game

    def __init__(self, board, speed):
        if speed < 1:
            raise ValueError("Speed must be at least 1")

        self.board = board
        self.speed = speed
        self.speed_mod = 0
        self.tick = 0
        self.tick_length = .05
        self.score = 0
        self.level = 0
        self.rows_cleared = 0
        self.game_over = False

    # Takes in key_press, returns the correct action
    def action(self, key_press):
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

    def action_update(self, action, next_pos):
        if not self.board.invalid_move(next_pos):  # validity check and update
            if self.board.debug:
                self.board.debug_window.addstr(11, 0, "valid move")
                self.board.debug_window.refresh()

            self.board.update_piece_position(action, next_pos)

    # new piece loop
    def new_piece_handler(self):
        next_piece = self.board.random_piece()

        if self.board.is_loss(next_piece):
            self.game_over = True
            return
        else:
            self.board.add_new_piece(next_piece)

    def piece_landed_handler(self):
        if self.board.is_loss(self.board.current_piece):  # check for lock or block
            self.game_over = True
            return
        else:
            full_rows = self.board.check_rows()

            if full_rows:
                self.update_state(full_rows)
                self.board.draw_score(self.score)
                self.board.draw_level(self.level)
                self.board.clear_and_move_rows()

            if self.board.debug:
                self.board.debug_window.addstr(3, 0, "New piece: {} ".format(True))

            self.new_piece_handler()

    # https://tetris.wiki/Scoring
    # Nintendo scoring
    def calculate_score(self, full_rows):
        lines_cleared = len(full_rows)

        line_mult = [40, 100, 300, 1200]

        score = line_mult[lines_cleared - 1] * (self.level + 1)

        return score

    def update_state(self, full_rows):
        self.rows_cleared += len(full_rows)
        self.level = self.rows_cleared // 5
        self.speed_mod = self.level * self.tick_length
        self.score += self.calculate_score(full_rows)

    def reset_engine_state(self):
        self.rows_cleared = 0
        self.level = 0
        self.speed_mod = 0
        self.score = 0
        self.tick = 0
        self.game_over = False

    def game_over_handler(self):
        self.board.draw_game_over()

        self.board.game_window.nodelay(False)

        while(self.game_over):
            key = self.board.get_input()

            if key == ord('y'):
                self.board.game_window.nodelay(True)
                self.reset_engine_state()
                self.board.reset_board_state()
            elif key == ord('n'):
                self.board.game_window.nodelay(True)
                self.exit_game()
            else:
                continue

    def control_loop(self):

        self.board.add_new_piece(self.board.random_piece())

        while(not self.game_over):
            if self.board.debug:
                self.board.debug_window.addstr(0, 0, "Tick: {}".format(self.tick))
                self.board.debug_window.refresh()

            self.board.draw_board()
            self.board.draw_score(self.score)
            self.board.draw_level(self.level)
            self.board.draw_next_piece()

            key_pressed = self.board.get_input()

            if self.board.debug:
                self.board.debug_window.addstr(1, 0, "Key pressed: {} ".format(key_pressed))
                self.board.debug_window.refresh()

            if key_pressed in (KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, ord('q')):

                self.action_update(*self.action(key_pressed))

                if self.board.piece_landed():
                    self.piece_landed_handler()
                    self.board.draw_next_piece()

            if self.tick % ((self.speed - self.speed_mod)
               // self.tick_length + 1) == 0:  # default movement

                self.action_update(None, self.board.gravity())
                if self.board.debug:
                    self.board.debug_window.addstr(2, 0, "Gravity: {}".format(self.tick))
                    self.board.debug_window.addstr(3, 0, "New piece: {}".format(False))
                    self.board.debug_window.refresh()

                if self.board.piece_landed():
                    self.piece_landed_handler()

            # https://stackoverflow.com/a/25251804
            time.sleep(self.tick_length - time.time() % self.tick_length)
            self.tick += 1

    def exit_game(self):
        exit(0)

    def run(self):

        try:
            while(True):
                self.control_loop()
                self.game_over_handler()

        except KeyboardInterrupt:
            self.exit_game()
