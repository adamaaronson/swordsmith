import sys
import time

# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../swordsmith')

import swordsmith as sw

def read_wordlist(filepath, dbpath, scored=True, min_score=50):
    words = open(filepath).read().splitlines()

    words = [w.upper() for w in words]

    if scored:
        words = [w.split(';') for w in words]
        words = [w[0] for w in words if int(w[1]) >= min_score]
    
    return sw.Wordlist(words, dbpath)

wl = read_wordlist('wordlist/spreadthewordlist.dict', 'wordlist/spreadthewordlist.db')

wl.init_database()

tic = time.time()
print(wl.get_database_matches('A.L.......R'))
print(time.time() - tic)

tic = time.time()
print(wl.get_matches('A.L....T..R'))
print(time.time() - tic)