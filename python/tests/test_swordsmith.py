import sys
import argparse
import time

# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../swordsmith')

import swordsmith as sw


def read_grid(filepath):
    return open(filepath).read().splitlines()


def read_wordlist(filepath, dbpath, scored=True, min_score=50):
    with open(filepath, 'r') as f:
        words = f.readlines()

    words = [w.upper() for w in words]

    if scored:
        words = [w.split(';') for w in words]
        words = [w[0] for w in words if len(w) == 1 or int(w[1]) >= min_score]
    
    return sw.Wordlist(words, dbpath)


def log_times(times):
    print(f'Took {sum(times) / len(times)} seconds on average over {len(times)} crosswords.')
    print(f'Min time: {min(times)} seconds')
    print(f'Max time: {max(times)} seconds')


def get_filler(args):
    if args.strategy == 'dfs':
        return sw.DFSFiller()
    elif args.strategy == 'minlook':
        return sw.MinlookFiller(args.k)
    else:
        return None


def run_test(args):
    wordlist = read_wordlist(args.wordlist_path, args.database_path)
    wordlist.init_database()
    
    grid = read_grid(args.grid_path)
    times = []

    for i in range(args.num_trials):
        tic = time.time()

        xword = sw.AmericanCrossword.from_grid(grid, wordlist)
        filler = get_filler(args)

        filler.fill(xword, args.animate)

        duration = time.time() - tic

        times.append(duration)

        if not args.animate:
            print(xword)
        
        print(f'Took {duration} seconds to fill {xword.cols}x{xword.rows} crossword.')
    
    log_times(times)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ye olde swordsmith test suite')
    
    parser.add_argument('-w', '--wordlist', dest='wordlist_path', type=str,
                        default='wordlist/spreadthewordlist.dict', help='filepath for wordlist')
    parser.add_argument('-d', '--database', dest='database_path', type=str,
                        default='wordlist/spreadthewordlist.db', help='filepath for wordlist database')
    parser.add_argument('-g', '--grid', dest='grid_path', type=str,
                        default='grids/15xcommon.txt', help='filepath for grid')
    parser.add_argument('-t', '--num_trials', dest='num_trials', type=int,
                        default=5, help='number of grids to try filling')
    parser.add_argument('-a', '--animate',
                        default=False, action='store_true', help='whether to animate grid filling')
    parser.add_argument('-s', '--strategy', dest='strategy', type=str,
                        default='dfs', help='which algorithm to run: dfs, minlook')
    parser.add_argument('-k', '--k', dest='k', type=int,
                        default=5, help='k constant for minlook')
    args = parser.parse_args()
    
    run_test(args)