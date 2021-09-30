import crossword as xw
from random import shuffle

size = 5

wordlist = [w.upper() for w in open('../crossword-scripts/allwords.txt').read().splitlines()]
# wordlist = [w.split(';') for w in wordlist]
# wordlist = [w[0] for w in wordlist if int(w[1]) >= 40]


wordlist = [w for w in wordlist if len(w) <= size]
shuffle(wordlist)

xword = xw.Crossword(size, size)

xword.put_block(0,0)
xword.put_block(4,4)

# xword.put_block(0,4)
# xword.put_block(1,4)
# xword.put_block(2,4)
# xword.put_block(6,4)
# xword.put_block(7,4)
# xword.put_block(8,4)
# xword.put_block(4,0)
# xword.put_block(4,1)
# xword.put_block(4,2)
# xword.put_block(4,6)
# xword.put_block(4,7)
# xword.put_block(4,8)

# for w in xword.down_crossings:
#     print(w, xword.down_crossings[w])

# print(xword)

xword.solve(wordlist, printout=True)