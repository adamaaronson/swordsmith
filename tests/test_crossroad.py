import sys
# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../crossroad')

import crossroad as xr
from random import shuffle
import time
import cProfile


def xword_15x(wordlist):
    xword = xr.Crossword(15, 15, wordlist)
    
    blocks1 = [
        (0, 5),
        (1, 5),
        (0, 11),
        (1, 11),
        (2, 11),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 8),
        (3, 9),
        (4, 7),
        (5, 6),
        (6, 5),
        (7, 4),
        (8, 3),
        (9, 0),
        (9, 1)
    ]

    blocks2 = []

    for (bx, by) in blocks1:
        blocks2.append((14 - bx, 14 - by))

    blocks = blocks1 + blocks2

    xword.put_blocks(blocks)
    
    return xword


def xword_9x(wordlist):
    xword = xr.Crossword(9, 9, wordlist)
    xword.put_block(0, 4)
    xword.put_block(1, 4)
    xword.put_block(2, 4)
    xword.put_block(6, 4)
    xword.put_block(7, 4)
    xword.put_block(8, 4)
    xword.put_block(4, 0)
    xword.put_block(4, 1)
    xword.put_block(4, 2)
    xword.put_block(4, 6)
    xword.put_block(4, 7)
    xword.put_block(4, 8)
    return xword


words = [w.upper() for w in open('wordlist/spreadthewordlist.dict').read().splitlines()]
words = [w.split(';') for w in words]
words = [w[0] for w in words if int(w[1]) >= 50]
wordlist = xr.Wordlist(words)

trials = 10
times = []

# cProfile.run("""

for i in range(trials):
    tic = time.time()

    xword = xword_15x(wordlist)
    xword.fill('dfs', printout=False)

    duration = time.time() - tic

    times.append(duration)

    print(xword)
    print(f'Took {duration} seconds to fill {xword.cols}x{xword.rows} crossword.')

# """)

print(f'Took {sum(times) / trials} seconds on average over {trials} crosswords.')