import sys
# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../crossroad')

import crossroad as xr
from random import shuffle
import time
import cProfile


def xword_15x(wordlist):
    grid = [
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [1,1,1,1,0,0,0,0,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,0,0,0,0,1,1,1,1],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0]
    ]
    
    return xr.Crossword.from_grid(grid, wordlist)


def xword_open(wordlist):
    grid = [
        [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0]
    ]

    return xr.Crossword.from_grid(grid, wordlist)


def xword_9x(wordlist):
    grid = [
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,1,1,1],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0]
    ]

    return xr.Crossword.from_grid(grid, wordlist)


def xword_7x(wordlist):
    grid = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]

    return xr.Crossword.from_grid(grid, wordlist)


words = [w.upper() for w in open('wordlist/spreadthewordlist.dict').read().splitlines()]
words = [w.split(';') for w in words]
words = [w[0] for w in words if int(w[1]) >= 50]
wordlist = xr.Wordlist(words)

trials = 1
animate = True
strategy = 'minlook'

times = []

# cProfile.run("""

for i in range(trials):
    tic = time.time()

    xword = xword_15x(wordlist)

    xword.fill(strategy=strategy, printout=animate)
    print(len(xword.entryset))

    duration = time.time() - tic

    times.append(duration)

    if not animate:
        print(xword)
    print(f'Took {duration} seconds to fill {xword.cols}x{xword.rows} crossword.')

# """)

print(f'Took {sum(times) / trials} seconds on average over {trials} crosswords.')
print(f'Min time: {min(times)} seconds')
print(f'Max time: {max(times)} seconds')