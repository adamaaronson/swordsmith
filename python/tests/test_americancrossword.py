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

with open('grids/15xcommon.txt', 'r') as f:
    grid = f.read().splitlines()


xw = sw.AmericanCrossword.from_grid(grid)

print(xw)

for slot in xw.words:
    print(slot, xw.words[slot])