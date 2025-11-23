import utils

import math
import argparse
import time
import os
import re

from abc import ABC, abstractmethod
from random import shuffle
from collections import defaultdict

EMPTY = '.'
BLOCK = ' '


class Crossword:
    def __init__(self):
        self.slots = set()
        """set of slots in the puzzle"""

        self.squares = defaultdict(lambda: defaultdict(int))
        """square => slots that contain it => index of square in slot"""

        self.crossings = defaultdict(lambda: defaultdict(tuple))
        """slot => slots that cross it => tuple of squares where they cross"""

        self.words = {}
        """slot => word in that slot"""

        self.wordset = set()
        """set of filled words in puzzle"""

        self.constraints = defaultdict(str)
        """slot => regex constraining words for that slot"""

    def __str__(self):
        return '\n'.join(
            ', '.join(str(square) for square in slot) + ': ' + self.words[slot]
            for slot in self.slots
        )

    def clear(self):
        """Resets the crossword by clearing all fields"""
        self.slots.clear()
        self.squares.clear()
        self.crossings.clear()
        self.words.clear()
        self.wordset.clear()

    def generate_crossings(self):
        for square in self.squares:
            for slot in self.squares[square]:
                for crossing_slot in self.squares[square]:
                    if slot != crossing_slot:
                        if crossings_tuple := self.crossings[slot][crossing_slot]:
                            self.crossings[slot][crossing_slot] = (
                                *crossings_tuple,
                                square,
                            )
                        else:
                            self.crossings[slot][crossing_slot] = (square,)

    def __put_letter_in_slot(self, letter, slot, i):
        """Sets letter at the given index of the given slot"""
        old_word = self.words[slot]
        if i >= len(slot):
            raise IndexError('Index greater than word length!')

        if old_word[i] == letter:
            # no change
            return

        new_word = old_word[0:i] + letter + old_word[i + 1 :]

        # update wordset
        if old_word in self.wordset:
            self.wordset.remove(old_word)
        if self.is_word_filled(new_word):
            self.wordset.add(new_word)

        # update words for just this slot, not crossing slots
        self.words[slot] = new_word

    def put_word(self, word, slot, wordlist_to_update=None):
        """Places word in the given slot, optionally adding it to the given wordlist"""
        if wordlist_to_update:
            wordlist_to_update.add_word(word)

        prev_word = self.words[slot]

        # place word in words map and wordset
        self.words[slot] = word
        if self.is_word_filled(prev_word):
            self.wordset.remove(prev_word)
        if self.is_word_filled(word):
            self.wordset.add(word)

        # update crossing words
        for crossing_slot in self.crossings[slot]:
            for square in self.crossings[slot][crossing_slot]:
                index = self.squares[square][slot]
                crossing_index = self.squares[square][crossing_slot]

                self.__put_letter_in_slot(word[index], crossing_slot, crossing_index)

    def add_constraint(self, slot, regex):
        """Add regex constraint to a given slot"""
        self.constraints[slot] = regex

    def is_dupe(self, word):
        """Returns whether or not a given word is already in the grid"""
        return word in self.wordset

    def is_filled(self):
        """Returns whether or not the whole crossword is filled"""
        return all(Crossword.is_word_filled(word) for word in self.words.values())

    def is_validly_filled(self, wordlist):
        """Returns whether the crossword is filled with words in the wordlist with no dupes"""
        if not self.is_filled():
            return False  # some unfilled words
        if not all(word in wordlist.words for word in self.words.values()):
            return False  # some invalid words
        if not len(self.wordset) == len(self.words.values()):
            return False  # some dupes
        if not all(
            re.search(constraint, self.words[slot])
            for slot, constraint in self.constraints.items()
        ):
            return False  # some constraint violations
        return True

    @staticmethod
    def is_word_filled(word):
        """Returns whether word is completely filled"""
        return EMPTY not in word


class AmericanCrossword(Crossword):
    def __init__(self, rows, cols):
        super(AmericanCrossword, self).__init__()

        self.rows = rows
        self.cols = cols
        self.grid = [
            [EMPTY for c in range(cols)] for r in range(rows)
        ]  # 2D array of squares

        self.__generate_slots_from_grid()

    @classmethod
    def from_grid(cls, grid, all_checked=True):
        """Generates AmericanCrossword from 2D array of characters"""
        rows = len(grid)
        cols = len(grid[0])

        blocks = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == BLOCK:
                    blocks.append((r, c))

        xw = cls(rows, cols)
        if blocks:
            xw.put_blocks(blocks)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != BLOCK and grid[r][c] != EMPTY:
                    xw.grid[r][c] = grid[r][c]

        xw.__generate_slots_from_grid(all_checked)

        return xw

    @staticmethod
    def is_across_slot(slot):
        return len({row for row, col in slot}) == 1

    @staticmethod
    def is_down_slot(slot):
        return len({col for row, col in slot}) == 1

    def get_clue_numbers_and_words(self):
        """Returns across words and down words and their numbers a la newspaper crosswords"""
        square_index = 1

        across_slots = set()
        down_slots = set()

        across_words = {}  # square index => slot
        down_words = {}  # square index => slot

        for row in range(self.rows):
            for col in range(self.cols):
                increment_index = False
                for slot in self.squares[(row, col)]:
                    if self.is_across_slot(slot) and slot not in across_slots:
                        across_slots.add(slot)
                        across_words[square_index] = self.words[slot]
                        increment_index = True
                    if self.is_down_slot(slot) and slot not in down_slots:
                        down_slots.add(slot)
                        down_words[square_index] = self.words[slot]
                        increment_index = True
                if increment_index:
                    square_index += 1

        return across_words, down_words

    def __generate_grid_from_slots(self):
        for slot in self.slots:
            for i, square in enumerate(slot):
                row, col = square
                self.grid[row][col] = self.words[slot][i]

    def __str__(self):
        self.__generate_grid_from_slots()
        return '\n'.join(' '.join([letter for letter in row]) for row in self.grid)

    def put_block(self, row, col):
        """Places block in certain square"""
        self.grid[row][col] = BLOCK
        self.__generate_slots_from_grid()

    def put_blocks(self, coords):
        """Places list of blocks in specified squares"""
        for row, col in coords:
            self.grid[row][col] = BLOCK
        self.__generate_slots_from_grid()

    def add_slot(self, squares, word):
        slot = tuple(squares)
        self.slots.add(slot)

        for i, square in enumerate(squares):
            self.squares[square][slot] = i

        if Crossword.is_word_filled(word):
            self.wordset.add(word)

        self.words[slot] = word

    def __generate_slots_from_grid(self, all_checked=True):
        self.clear()

        # generate across words
        for r in range(self.rows):
            word = ''
            squares = []
            for c in range(self.cols):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    # add a letter to the current word
                    word += letter
                    squares.append((r, c))
                else:
                    # block hit, check to see if there's a word in progress
                    if word != '':
                        if all_checked or len(squares) > 1:
                            self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in row
            if word != '':
                if all_checked or len(squares) > 1:
                    self.add_slot(squares, word)

        # generate down words
        for c in range(self.cols):
            word = ''
            squares = []
            for r in range(self.rows):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    # add a letter to the current word
                    word += letter
                    squares.append((r, c))
                else:
                    # block hit, check to see if there's a word in progress
                    if word != '':
                        if all_checked or len(squares) > 1:
                            self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in column
            if word != '':
                if all_checked or len(squares) > 1:
                    self.add_slot(squares, word)

        self.generate_crossings()


class Wordlist:
    """Collection of words to be used for filling a crossword"""

    def __init__(self, words):
        self.words = set(words)
        self.added_words = set()

        # mapping from wildcard patterns to lists of matching words, used for memoization
        self.pattern_matches = {}

        # mapping from length to index to letter to wordset
        # this stores an n-letter word n times, so might be memory intensive but we'll see
        self.indices = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

        # mapping from length to wordset
        self.lengths = defaultdict(set)

        self.__init_indices()

    def __init_indices(self):
        for word in self.words:
            self.__add_word_to_indices(word)

    def __add_word_to_indices(self, word):
        length = len(word)
        self.lengths[length].add(word)
        for i, letter in enumerate(word):
            self.indices[length][i][letter].add(word)

    def __remove_word_from_indices(self, word):
        length = len(word)
        self.lengths[length].remove(word)
        for i, letter in enumerate(word):
            self.indices[length][i][letter].remove(word)

    def add_word(self, word):
        if word not in self.words:
            self.words.add(word)
            self.added_words.add(word)
            self.__add_word_to_indices(word)

    def remove_word(self, word):
        if word in self.words:
            self.words.remove(word)
            self.__remove_word_from_indices(word)
        if word in self.added_words:
            self.added_words.remove(word)

    def get_matches(self, pattern, regex):
        if (pattern, regex) in self.pattern_matches:
            return self.pattern_matches[(pattern, regex)]

        length = len(pattern)
        indices = [
            self.indices[length][i][letter]
            for i, letter in enumerate(pattern)
            if letter != EMPTY
        ]
        if indices:
            matches = set.intersection(*indices)
        else:
            matches = self.lengths[length]

        if regex:
            matches = [match for match in matches if re.search(regex, match)]

        self.pattern_matches[(pattern, regex)] = matches

        return matches


class RetryException(Exception):
    """Exceeded retry time"""


class Filler(ABC):
    """Abstract base class containing useful methods for filling crosswords"""

    @abstractmethod
    def fill(self, crossword, wordlist, animate, retry_time=None):
        """Fills the given crossword using some strategy"""

    @staticmethod
    def get_new_crossing_words(crossword, slot, word):
        """
        Returns list of (crossing slot, new word) that cross the given slot,
        given a word to theoretically put in the slot. Excludes slots that were already filled.
        """
        new_crossing_words = []

        for crossing_slot in crossword.crossings[slot]:
            new_crossing_word = crossword.words[crossing_slot]
            for square in crossword.crossings[slot][crossing_slot]:
                index = crossword.squares[square][slot]
                letter = word[index]

                crossing_index = crossword.squares[square][crossing_slot]
                crossing_word = crossword.words[crossing_slot]

                new_crossing_word = (
                    new_crossing_word[:crossing_index]
                    + letter
                    + new_crossing_word[crossing_index + 1 :]
                )

            if (
                Crossword.is_word_filled(crossing_word)
                and crossing_word == new_crossing_word
            ):
                # this word was already there, ignore
                continue

            new_crossing_words.append((crossing_slot, new_crossing_word))

        return new_crossing_words

    @staticmethod
    def is_valid_match(crossword, wordlist, slot, match):
        """Returns whether the match can be placed in the slot without creating a dupe or invalid word."""

        if match not in wordlist.words:
            return False  # match is invalid word
        if crossword.is_dupe(match):
            return False  # match is dupe

        new_crossing_words = Filler.get_new_crossing_words(crossword, slot, match)

        # make sure crossing words are valid
        for _, crossing_word in new_crossing_words:
            if (
                Crossword.is_word_filled(crossing_word)
                and crossing_word not in wordlist.words
            ):
                return False  # created invalid word
            if crossword.is_dupe(crossing_word):
                return False  # created dupe

        # make sure crossing words don't dupe each other
        if len(set(new_crossing_words)) != len(new_crossing_words):
            return False

        return True

    @staticmethod
    def fewest_matches(crossword, wordlist):
        """Finds the slot that has the fewest possible matches, this is probably the best next place to look."""
        fewest_matches_slot = None
        fewest_matches = len(wordlist.words) + 1

        for slot in crossword.words:
            word = crossword.words[slot]
            if Crossword.is_word_filled(word):
                continue
            matches = len(wordlist.get_matches(word, crossword.constraints[slot]))
            if matches < fewest_matches:
                fewest_matches = matches
                fewest_matches_slot = slot
        return fewest_matches_slot, fewest_matches

    @staticmethod
    def minlook(crossword, wordlist, slot, matches, k):
        """Considers given matches, returns index of the one that offers the most possible crossing words. If there are none, returns -1"""
        match_indices = range(min(k, len(matches)))  # just take first k matches
        failed_indices = set()

        best_match_index = -1
        best_cross_product = -1

        for match_index in match_indices:
            cross_product = 0

            for crossing_slot, crossing_word in Filler.get_new_crossing_words(
                crossword, slot, matches[match_index]
            ):
                num_matches = len(
                    wordlist.get_matches(
                        crossing_word, crossword.constraints[crossing_slot]
                    )
                )

                # if no matches for some crossing slot, give up and move on
                # this is basically "arc-consistency lookahead"
                if num_matches == 0:
                    failed_indices.add(match_index)
                    cross_product = float('-inf')
                    break

                # use log product to avoid explosions
                cross_product += math.log(num_matches)

            if cross_product > best_cross_product:
                best_match_index = match_index
                best_cross_product = cross_product

        return best_match_index, failed_indices


class DFSFiller(Filler):
    """
    Fills the crossword using a naive DFS algorithm:

    - keeps selecting unfilled slot with fewest possible matches
    - randomly chooses matching word for that slot
    - backtracks if there is a slot with no matches
    """

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            utils.clear_terminal()
            print(crossword)

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if crossword.is_filled():
            return True

        # choose slot with fewest matches
        slot, num_matches = Filler.fewest_matches(crossword, wordlist)

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False

        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.words[slot]
        matches = wordlist.get_matches(
            crossword.words[slot], crossword.constraints[slot]
        )

        # randomly shuffle matches
        matches = list(matches)
        shuffle(matches)

        for match in matches:
            if not Filler.is_valid_match(crossword, wordlist, slot, match):
                continue

            crossword.put_word(match, slot)

            if self.fill(crossword, wordlist, animate, retry_time):
                return True

        # if no match works, restore previous word
        crossword.put_word(previous_word, slot)

        return False


class DFSBackjumpFiller(Filler):
    """
    Fills the crossword using a naive DFS algorithm:

    - keeps selecting unfilled slot with fewest possible matches
    - randomly chooses matching word for that slot
    - backtracks if there is a slot with no matches

    Each iteration returns (is_filled, failed_slot)
    """

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            utils.clear_terminal()
            print(crossword)

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if crossword.is_filled():
            return True, None

        # choose slot with fewest matches
        slot, num_matches = Filler.fewest_matches(crossword, wordlist)

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False, slot

        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.words[slot]
        matches = wordlist.get_matches(
            crossword.words[slot], crossword.constraints[slot]
        )

        # randomly shuffle matches
        matches = list(matches)
        shuffle(matches)

        for match in matches:
            if not Filler.is_valid_match(crossword, wordlist, slot, match):
                continue

            crossword.put_word(match, slot)

            is_filled, failed_slot = self.fill(crossword, wordlist, animate, retry_time)
            if is_filled:
                return True, None
            if failed_slot not in crossword.crossings[slot]:
                # undo this word, keep backjumping
                crossword.put_word(previous_word, slot)
                return False, failed_slot

        # if no match works, restore previous word
        crossword.put_word(previous_word, slot)
        return False, slot


class MinlookFiller(Filler):
    """
    Fills the crossword using a dfs algorithm with minlook heuristic:
    - keeps selecting unfilled slot with fewest possible matches
    - considers k random matching word, chooses word with the most possible crossing words (product of # in each slot)
    - backtracks if there is a slot with no matches
    """

    def __init__(self, k):
        self.k = k

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            utils.clear_terminal()
            print(crossword)

        # if the grid is filled, succeed
        if crossword.is_filled():
            return True

        # choose slot with fewest matches
        slot, num_matches = Filler.fewest_matches(crossword, wordlist)

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False

        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.words[slot]
        matches = wordlist.get_matches(
            crossword.words[slot], crossword.constraints[slot]
        )

        # randomly shuffle matches
        matches = list(matches)
        shuffle(matches)

        while matches:
            match_index, failed_indices = Filler.minlook(
                crossword, wordlist, slot, matches, self.k
            )

            if match_index != -1:
                match = matches[match_index]

            # remove failed matches and chosen match
            matches = [
                matches[i]
                for i in range(len(matches))
                if i != match_index and i not in failed_indices
            ]

            # if no matches were found, try another batch if possible
            if match_index == -1:
                continue

            if not Filler.is_valid_match(crossword, wordlist, slot, match):
                continue

            crossword.put_word(match, slot)

            if self.fill(crossword, wordlist, animate, retry_time):
                return True

        # if no match works, restore previous word
        crossword.put_word(previous_word, slot)
        return False


class MinlookBackjumpFiller(Filler):
    """
    Fills the crossword using a dfs algorithm with minlook heuristic:
    - keeps selecting unfilled slot with fewest possible matches
    - considers k random matching word, chooses word with the most possible crossing words (product of # in each slot)
    - backtracks if there is a slot with no matches

    Each iteration returns (is_filled, failed_slot)
    """

    def __init__(self, k):
        self.k = k

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            utils.clear_terminal()
            print(crossword)

        # if the grid is filled, succeed
        if crossword.is_filled():
            return True, None

        # choose slot with fewest matches
        slot, num_matches = Filler.fewest_matches(crossword, wordlist)

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False, slot

        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.words[slot]
        matches = wordlist.get_matches(
            crossword.words[slot], crossword.constraints[slot]
        )

        # randomly shuffle matches
        matches = list(matches)
        shuffle(matches)

        while matches:
            match_index, failed_indices = Filler.minlook(
                crossword, wordlist, slot, matches, self.k
            )

            if match_index != -1:
                match = matches[match_index]

            # remove failed matches and chosen match
            matches = [
                matches[i]
                for i in range(len(matches))
                if i != match_index and i not in failed_indices
            ]

            # if no matches were found, try another batch if possible
            if match_index == -1:
                continue

            if not Filler.is_valid_match(crossword, wordlist, slot, match):
                continue

            crossword.put_word(match, slot)

            is_filled, failed_slot = self.fill(crossword, wordlist, animate, retry_time)
            if is_filled:
                return True, None
            if failed_slot not in crossword.crossings[slot]:
                # undo this word, keep backjumping
                crossword.put_word(previous_word, slot)
                return False, failed_slot

        # if no match works, restore previous word
        crossword.put_word(previous_word, slot)
        return False, slot


class Miner:
    """
    Wrapper for a filler that repeatedly tries the filler,
    retrying after a given number of seconds.
    """

    def __init__(self, filler: Filler, retry_seconds: int):
        self.filler = filler
        self.retry_seconds = retry_seconds

    def fill(self, crossword_maker, wordlist, animate):
        retries = 0

        while True:
            retry_time = time.time() + self.retry_seconds
            crossword = crossword_maker()

            try:
                self.filler.fill(crossword, wordlist, animate, retry_time)
                break
            except RetryException:
                retries += 1
                print(f'Attempt #{retries} timed out. Retrying.')

        print(crossword)


WORDLIST_FOLDER = 'wordlist/'
GRID_FOLDER = 'grid/'
GRID_SUFFIX = '.txt'


def read_grid(filepath):
    with open(filepath, 'r') as f:
        return f.read().splitlines()


def read_wordlist(filepath, scored=True, min_score=50):
    with open(filepath, 'r') as f:
        words = f.readlines()

    words = [w.upper() for w in words]

    if scored:
        words = [w.split(';') for w in words]
        words = [w[0] for w in words if len(w) == 1 or int(w[1]) >= min_score]

    return Wordlist(words)


def log_times(times, strategy):
    print(f'Filled {len(times)} crosswords using {strategy}')
    print(f'Min time: {min(times):.4f} seconds')
    print(f'Avg time: {sum(times) / len(times):.4f} seconds')
    print(f'Max time: {max(times):.4f} seconds')


def get_filler(args):
    if args.strategy == 'dfs':
        return DFSFiller()
    elif args.strategy == 'dfsb':
        return DFSBackjumpFiller()
    elif args.strategy == 'minlook':
        return MinlookFiller(args.k)
    elif args.strategy == 'mlb':
        return MinlookBackjumpFiller(args.k)
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
    parser = argparse.ArgumentParser(description='ye olde swordsmith engine')

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
        '-t',
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


if __name__ == '__main__':
    main()
