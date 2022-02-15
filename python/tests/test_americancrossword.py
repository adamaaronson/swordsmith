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

slot = ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0))
print(slot)

xw = sw.AmericanCrossword.from_grid(grid)

print(xw)