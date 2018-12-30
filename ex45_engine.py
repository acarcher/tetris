# Driver and state transitions
import time
import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_ENTER, ERR
# from sys import exit


class Engine(object):

    # board: board to play
    # speed: how many seconds per action (period)
    # score: points earned
    # tick_length: period of the game

    def __init__(self, board, speed):
        assert(speed >= 1)
        self.board = board
        self.speed = speed
        self.speed_mod = 0
        self.score = 0
        self.level = 0
        self.rows_cleared = 0
        self.tick_length = .05

    # Takes in key_press, returns the correct action
    def action(self, key_press):
        move_keys = (KEY_RIGHT, KEY_LEFT, KEY_DOWN)

        rotate_key = (KEY_UP,)

        if key_press == ord('q'):
            self.end()
        elif key_press in move_keys:
            return key_press, self.board.current_piece.move(key_press)
        elif key_press in rotate_key:
            return key_press, self.board.current_piece.rotate_clockwise()
        else:
            # raise Exception("Key unbound")
            pass
            # TODO

    def action_update(self, action, next_pos):
        if not self.board.invalid_move(next_pos):  # validity check and update
            if self.board.debug:
                self.board.debug_window.addstr(11, 0, "valid move")
                self.board.debug_window.refresh()
            self.board.update_piece_position(action, next_pos)
        else:
            # raise Exception("Illegal move")
            # TODO
            pass

    # new piece loop
    def new_piece_handler(self, init=False):
        next_piece = self.board.random_piece(random.randint(0, 6))
        #TODO: IMPROVE
        if init:
            self.board.next_piece = next_piece
            self.board.add_new_piece(self.board.random_piece(random.randint(0, 6)))

        elif not init and self.board.is_loss(next_piece):
            self.board.game_over()
            # break FIXME
        else:
            self.board.add_new_piece(next_piece)

    def piece_landed_handler(self):
        if self.board.is_loss(self.board.current_piece):  # check for lock or block
            self.board.game_over()  # FIXME
            raise Exception("Game over")  # FIXME
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

    # TODO:
    def run(self):

        self.board.init_curses()

        tick = 0
        game_over = False
        key_pressed = None
        self.new_piece_handler(True)

        while(not game_over):
            if self.board.debug:
                self.board.debug_window.addstr(0, 0, "Tick: {}".format(tick))
                self.board.debug_window.refresh()

            self.board.draw_board()  # draw
            self.board.draw_score(self.score)
            self.board.draw_level(self.level)
            self.board.draw_next_piece()

            key_pressed = self.board.get_input()  # take input

            if self.board.debug:
                self.board.debug_window.addstr(1, 0, "Key pressed: {} ".format(key_pressed))
                self.board.debug_window.refresh()

            # if key_pressed != ERR and key_pressed is not None:
            if key_pressed in (KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP):

                self.action_update(*self.action(key_pressed))

                if self.board.piece_landed():  # piece is done moving
                    self.piece_landed_handler()
                    self.board.draw_next_piece()

            if tick % ( (self.speed - self.speed_mod) // self.tick_length + 1) == 0:  # default movement
                self.action_update(None, self.board.gravity())
                if self.board.debug:
                    self.board.debug_window.addstr(2, 0, "Gravity: {}".format(tick))
                    self.board.debug_window.addstr(3, 0, "New piece: {}".format(False))
                    self.board.debug_window.refresh()

                if self.board.piece_landed():  # piece is done moving
                    self.piece_landed_handler()

            # https://stackoverflow.com/a/25251804
            time.sleep(self.tick_length - time.time() % self.tick_length)
            tick += 1
