import sys
import time

# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../swordsmith')

import swordsmith as sw

xw = sw.AmericanCrossword(5, 5)
print(xw)
for s in xw.squares:
    for slot in xw.squares[s]:
        print(s, slot, xw.squares[s][slot])