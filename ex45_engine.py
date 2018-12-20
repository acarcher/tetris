# Driver and state transitions
import time
import curses
import random
from sys import exit


class Engine(object):

    # board: board to play
    # speed: how many seconds per action
    # score: points earned
    # tick_length: period of the game

    def __init__(self, board, speed):
        assert(speed >= 1)
        self.board = board
        self.speed = speed
        self.score = 0
        self.tick_length = .05

    # Takes in key_press, returns the correct action
    def action(self, key_press):
        move_keys = (curses.KEY_RIGHT, curses.KEY_LEFT,
                     curses.KEY_DOWN)

        rotate_key = (curses.KEY_UP,)

        if key_press == ord('q'):
            self.end()
        elif key_press in move_keys:
            return self.board.current_piece.move(key_press)
        elif key_press in rotate_key:
            return self.board.current_piece.rotate_clockwise()
        else:
            raise Exception("Key unbound")
            pass
            #TODO

    # validation loop
    # valid move?
    #   update piece pos
    #   return False
    # piece landed
    #   loss?
    #       game_over
    #   return True
    # other invalid move
    #
    # Take in action output, returns new_piece bool
    # TODO: make nicer
    def action_update(self, next_pos):
        if not self.board.invalid_move(next_pos):  # validity check and update
            self.board.screen.addstr(11, 20, "valid move")
            self.board.screen.refresh()
            self.board.update_piece_position(next_pos)
        else:
            # raise Exception("Illegal move")
            # TODO
            pass

    # new piece loop
    def new_piece_handler(self, init=False):
        next_piece = self.board.random_piece(random.randint(0, 6))

        if not init and self.board.is_loss(next_piece):
            self.board.game_over()
            # break FIXME
        else:
            self.board.add_new_piece(next_piece)

    # TODO
    def run(self):

        self.board.init_colors()
        self.board.screen.nodelay(True)
        curses.curs_set(False)

        tick = 0
        game_over = False
        key_pressed = None
        self.new_piece_handler(True)

        while(not game_over):

            self.board.screen.addstr(0, 20, "Tick: {}".format(tick))
            self.board.screen.refresh()

            new_piece = False

            self.board.draw()  # draw

            key_pressed = self.board.get_input()  # take input

            if key_pressed != curses.ERR and key_pressed is not None:
                self.board.screen.addstr(1, 20, "Key pressed: {}".format(key_pressed))
                self.board.screen.refresh()

                self.action_update(self.action(key_pressed))

                if self.board.piece_landed():  # piece is done moving
                    if self.board.is_loss(self.board.current_piece):  # check for lock or block
                        self.board.game_over()  # FIXME
                        raise Exception("Game over")  # FIXME
                    else:
                        full_rows = self.board.check_rows()  # check to see if finished rows

                        if full_rows:  # update score and clear full rows
                            self.score += len(full_rows)
                            self.board.clear_full_rows(full_rows)
                        new_piece = True

            if new_piece:  # generate and add the new piece TODO
                self.new_piece_handler()
                new_piece = False

            if tick % (self.speed // self.tick_length + 1) == 0:  # default movement
                self.action_update(self.board.gravity())

                self.board.screen.addstr(2, 20, "Gravity: {}".format(tick))
                self.board.screen.addstr(3, 20, "New piece: {}".format(new_piece))
                self.board.screen.refresh()

                if self.board.piece_landed():  # piece is done moving
                    if self.board.is_loss(self.board.current_piece):  # check for lock or block
                        self.board.game_over()  # FIXME
                        raise Exception("Game over")  # FIXME
                    else:
                        full_rows = self.board.check_rows()  # check to see if finished rows

                        if full_rows:  # update score and clear full rows
                            self.score += len(full_rows)
                            self.board.clear_full_rows(full_rows)
                        new_piece = True

                # TODO
                if new_piece:  # generate and add the new piece TODO
                    self.new_piece_handler()
                    new_piece = False

            # https://stackoverflow.com/a/25251804
            time.sleep(self.tick_length - time.time() % self.tick_length)
            tick += 1
