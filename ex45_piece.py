from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN
import ex45_config


# Base representation for each tetromino
# Pieces can be moved and rotated

class Piece(object):

    tetromino_attributes = {
        "I": ("cyan", "@", 4),
        "J": ("blue", "#", 3),
        "L": ("white", "$", 3),
        "O": ("yellow", "%", 2),
        "S": ("green", "&", 3),
        "T": ("magenta", "+", 3),
        "Z": ("red", "=", 3)
    }

    tetromino_orientations = {
        "I": ex45_config.i_map,
        "J": ex45_config.j_map,
        "L": ex45_config.l_map,
        "O": ex45_config.o_map,
        "S": ex45_config.s_map,
        "T": ex45_config.t_map,
        "Z": ex45_config.z_map
    }

    def __init__(self, tetromino, location=None):
        self.tetromino = tetromino
        self.color, self.symbol, self.extent = self.tetromino_attributes[tetromino]
        self.orientation = 0
        self.location = location  # [[y,x], [y,x], [y,x], [y,x]]

    # Takes in a key_press, returns coords
    def move(self, key_press):
        if key_press == KEY_RIGHT:
            return [[point[0], point[1] + 1] for point in self.location]

        elif key_press == KEY_LEFT:
            return [[point[0], point[1] - 1] for point in self.location]

        elif key_press == KEY_DOWN:
            return [[point[0] + 1, point[1]] for point in self.location]

    # http://tetris.wikia.com/wiki/SRS
    # FIXME
    def rotate_clockwise(self):
        orientation_transform = self._next_orientation()

        return [[point[0] + transform[0], point[1] + transform[1]]
                for point, transform in zip(self.location, orientation_transform)]

        # https://stackoverflow.com/a/1996601 &
        # https://stackoverflow.com/a/1996506
        # return [[1 - (point[1] - (self.extent - 2)), point[0]]
        #         for point in self.location]
        # return [[point[1], 1 - (point[0] - (self.extent - 2))]
        #         for point in self.location]

    def _next_orientation(self):
        mapping = self.tetromino_orientations[self.tetromino]

        transform = mapping[self.orientation]

        self.orientation = (self.orientation + 1) % 4

        return transform
