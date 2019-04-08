# needs more explanation
SPEED = .75  # .75 is the speed, lower is harder, higher is easier
DEBUG = False
CHAR = b'\xe2\x96\xa0'
TICK_LENGTH = .05
HEIGHT = 20
WIDTH = 10

i_rotate_map = [
    [[-1, 2], [0, 1], [1, 0], [2, -1]],
    [[2, 1], [1, 0], [0, -1], [-1, -2]],
    [[1, -2], [0, -1], [-1, 0], [-2, 1]],
    [[-2, -1], [-1, 0], [0, 1], [1, 2]]
]

j_rotate_map = [
    [[0, 2], [-1, 1], [0, 0], [1, -1]],
    [[2, 0], [1, 1], [0, 0], [-1, -1]],
    [[0, -2], [1, -1], [0, 0], [-1, 1]],
    [[-2, 0], [-1, -1], [0, 0], [1, 1]]
]

l_rotate_map = [
    [[2, 0], [-1, 1], [0, 0], [1, -1]],
    [[0, -2], [1, 1], [0, 0], [-1, -1]],
    [[-2, 0], [1, -1], [0, 0], [-1, 1]],
    [[0, 2], [-1, -1], [0, 0], [1, 1]]
]

o_rotate_map = [
    [[0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0]]
]

s_rotate_map = [
    [[1, 1], [2, 0], [-1, 1], [0, 0]],
    [[1, -2], [0, -1], [1, 1], [0, 0]],
    [[-2, 0], [-1, -1], [1, -1], [0, 0]],
    [[0, 1], [-1, 2], [-1, -1], [0, 0]]
]

t_rotate_map = [
    [[1, 1], [-1, 1], [0, 0], [1, -1]],
    [[1, -1], [1, 1], [0, 0], [-1, -1]],
    [[-1, -1], [1, -1], [0, 0], [-1, 1]],
    [[-1, 1], [-1, -1], [0, 0], [1, 1]]
]

z_rotate_map = [
    [[0, 2], [1, 1], [0, 0], [1, -1]],
    [[2, 0], [1, -1], [0, 0], [-1, -1]],
    [[0, -2], [-1, -1], [0, 0], [-1, 1]],
    [[-2, 0], [-1, 1], [0, 0], [1, 1]]
]
