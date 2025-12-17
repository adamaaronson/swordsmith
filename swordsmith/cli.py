import argparse
import time
import os

from .crossword import AmericanCrossword
from .filler import DFSFiller, MinlookFiller
from .wordlist import read_wordlist


WORDLIST_FOLDER = 'wordlist/'
GRID_FOLDER = 'grid/'
GRID_SUFFIX = '.txt'


def read_grid(filepath):
    with open(filepath, 'r') as f:
        return f.read().splitlines()


def log_times(times, strategy):
    print(f'Filled {len(times)} crosswords using {strategy}')
    print(f'Min time: {min(times):.4f} seconds')
    print(f'Avg time: {sum(times) / len(times):.4f} seconds')
    print(f'Max time: {max(times):.4f} seconds')


def get_filler(args):
    if args.strategy == 'dfs':
        return DFSFiller()
    elif args.strategy == 'minlook':
        return MinlookFiller(args.k)
    else:
        return None


def run(args):
    dirname = os.path.dirname(__file__)
    wordlist_path_prefix = os.path.join(dirname, WORDLIST_FOLDER)
    grid_path_prefix = os.path.join(dirname, GRID_FOLDER)

    wordlist = read_wordlist(
        args.wordlist_path or wordlist_path_prefix + 'spreadthewordlist.dict',
        min_score=args.min_score,
    )

    grid_path = grid_path_prefix + args.grid_path
    if not grid_path.endswith(GRID_SUFFIX):
        grid_path = grid_path + GRID_SUFFIX

    grid = read_grid(grid_path)
    times = []

    for _ in range(args.num_trials):
        tic = time.time()

        crossword = AmericanCrossword.from_grid(grid)
        filler = get_filler(args)

        filler.fill(crossword, wordlist, args.animate)

        duration = time.time() - tic

        times.append(duration)

        if not args.animate:
            print(crossword)

        print(
            f'\nFilled {crossword.cols}x{crossword.rows} crossword in {duration:.4f} seconds\n'
        )

    log_times(times, args.strategy)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-w',
        '--wordlist',
        dest='wordlist_path',
        type=str,
        default=None,
        help='filepath for wordlist',
    )
    parser.add_argument(
        '-m',
        '--min-score',
        dest='min_score',
        type=int,
        default=50,
        help='minimum word score',
    )
    parser.add_argument(
        '-g',
        '--grid',
        dest='grid_path',
        type=str,
        default='15xcommon.txt',
        help='filepath for grid',
    )
    parser.add_argument(
        '-n',
        '--num-trials',
        dest='num_trials',
        type=int,
        default=5,
        help='number of grids to try filling',
    )
    parser.add_argument(
        '-a',
        '--animate',
        default=False,
        action='store_true',
        help='whether to animate grid filling',
    )
    parser.add_argument(
        '-s',
        '--strategy',
        dest='strategy',
        type=str,
        default='dfs',
        help='which algorithm to run: dfs, dfsb, minlook, mlb',
    )
    parser.add_argument(
        '-k', '--k', dest='k', type=int, default=5, help='k constant for minlook'
    )
    parser.add_argument(
        '-r',
        '--retry-seconds',
        dest='retry_seconds',
        type=float,
        default=None,
        help='number of seconds after which to reshuffle wordlist and retry',
    )
    args = parser.parse_args()

    run(args)
