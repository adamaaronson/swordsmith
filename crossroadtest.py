import crossroad as xr
from random import shuffle

words = [w.upper() for w in open('words/spreadthewordlist.dict').read().splitlines()]
words = [w.split(';') for w in words]
words = [w[0] for w in words if int(w[1]) >= 40]
shuffle(words)

wordlist = xr.Wordlist(words)

xword = xr.Crossword(9, 9)

xword.set_wordlist(wordlist)

xword.put_block(0,4)
xword.put_block(1,4)
xword.put_block(2,4)
xword.put_block(6,4)
xword.put_block(7,4)
xword.put_block(8,4)
xword.put_block(4,0)
xword.put_block(4,1)
xword.put_block(4,2)
xword.put_block(4,6)
xword.put_block(4,7)
xword.put_block(4,8)

# for w in xword.down_crossings:
#     print(w, xword.down_crossings[w])

# print(xword)


xword.solve_dfs(printout=True)

xword.print_words()