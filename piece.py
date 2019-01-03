from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN

import config

# Base representation for each tetromino
# Pieces can be moved and rotated

CHAR = b'\xe2\x96\xa0'


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

    symbol_to_color = {
        "@": "cyan",
        "#": "blue",
        "$": "white",
        "%": "yellow",
        "&": "green",
        "+": "magenta",
        "=": "red",
        "default": "default"
    }

    tetromino_orientations = {
        "I": config.i_rotate_map,
        "J": config.j_rotate_map,
        "L": config.l_rotate_map,
        "O": config.o_rotate_map,
        "S": config.s_rotate_map,
        "T": config.t_rotate_map,
        "Z": config.z_rotate_map
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

        return transform
