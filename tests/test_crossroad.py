import crossroad as xr
from random import shuffle
import time

words = [w.upper() for w in open('wordlist/spreadthewordlist.dict').read().splitlines()]
words = [w.split(';') for w in words]
words = [w[0] for w in words if int(w[1]) >= 50]
shuffle(words)

wordlist = xr.Wordlist(words)

def xword_15x15():
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

    for b in blocks:
        xword.put_block(*b)
    
    return xword


def xword_9x9():
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


def xword_5x5():
    return xr.Crossword(5, 5, wordlist)



tic = time.time()

xword = xword_5x5()
xword.fill('dfs', printout=True)

toc = time.time()

print(f'\nTook {toc - tic} seconds to fill.')