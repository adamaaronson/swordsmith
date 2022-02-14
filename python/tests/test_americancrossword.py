import sys
import time

# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../swordsmith')

import swordsmith as sw

grid = [
    'BLACK',
    '.....',
    '.....',
    '.....',
    '.....'
]

xw = sw.AmericanCrossword.from_grid(grid)

print(xw)