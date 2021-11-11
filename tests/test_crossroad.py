import sys
import argparse
import time

# TODO: better way to properly import stuff than this. this sucks
sys.path.append('../crossroad')

import crossroad as xr


def read_grid(filepath, block='#'):
    grid = open(filepath).read().splitlines()
    grid = [[1 if char == block else 0 for char in line] for line in grid]
    return grid


def read_wordlist(filepath, scored=True, min_score=50):
    words = open(filepath).read().splitlines()

    words = [w.upper() for w in words]

    if scored:
        words = [w.split(';') for w in words]
        words = [w[0] for w in words if int(w[1]) >= min_score]
    
    return xr.Wordlist(words)


def log_times(times):
    print(f'Took {sum(times) / len(times)} seconds on average over {len(times)} crosswords.')
    print(f'Min time: {min(times)} seconds')
    print(f'Max time: {max(times)} seconds')


def run_test(args):
    wordlist = read_wordlist(args.wordlist_path)
    grid = read_grid(args.grid_path)
    times = []

    for i in range(args.num_trials):
        tic = time.time()

        xword = xr.Crossword.from_grid(grid, wordlist)
        xword.fill(strategy=args.strategy, k=5, printout=args.animate)

        duration = time.time() - tic

        times.append(duration)

        if not args.animate:
            print(xword)
        
        print(f'Took {duration} seconds to fill {xword.cols}x{xword.rows} crossword.')
    
    log_times(times)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ye olde crossroad test suite')
    
    parser.add_argument('-w', '--wordlist', dest='wordlist_path', type=str, default='wordlist/spreadthewordlist.dict', help='filepath for wordlist')
    parser.add_argument('-g', '--grid', dest='grid_path', type=str, help='filepath for grid')
    parser.add_argument('-t', '--num_trials', dest='num_trials', type=int, default=5, help='number of grids to try filling')
    parser.add_argument('-a', '--animate', dest='animate', type=bool, default=False, help='whether to animate grid filling')
    parser.add_argument('-s', '--strategy', dest='strategy', type=str, default='dfs',
                        help='which algorithm to run: dfs, minlook')
    args = parser.parse_args()
    
    if not args.wordlist_path or not args.grid_path:
        sys.exit('You must specify grid path!')
    
    run_test(args)