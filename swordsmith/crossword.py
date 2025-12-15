from collections import defaultdict
import re

from constants import BLOCK, EMPTY


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

        self.regex_constraints = defaultdict(str)
        """slot => regex constraining words for that slot"""

        self.score_constraints = defaultdict(int)
        """slot => minimum score for words in that slot"""

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

    def add_regex_constraint(self, slot, regex):
        """Add regex constraint to a given slot"""
        if slot not in self.slots:
            raise ValueError(f'{slot} is not a valid slot')
        self.regex_constraints[slot] = regex

    def add_score_constraint(self, slot, score):
        """Add score constraint to a given slot"""
        if slot not in self.slots:
            raise ValueError(f'{slot} is not a valid slot')
        self.score_constraints[slot] = score

    def fits_regex_constraint(self, slot, word):
        """Returns whether the word fits that slot's regex constraint"""
        if slot not in self.regex_constraints:
            return True
        return re.search(self.regex_constraints[slot], word) is not None

    def fits_score_constraint(self, slot, word, wordlist):
        """Returns whether the word fits that slot's score constraint"""
        if slot not in self.score_constraints:
            return True
        return wordlist.scores[word] >= self.score_constraints[slot]

    def fits_constraints(self, slot, word, wordlist):
        """Returns whether the word fits all of that slot's constraints"""
        if not self.fits_regex_constraint(slot, word):
            return False
        if not self.fits_score_constraint(slot, word, wordlist):
            return False

        return True

    def is_dupe(self, word):
        """Returns whether or not a given word is already in the grid"""
        return word in self.wordset

    def is_filled(self):
        """Returns whether or not the whole crossword is filled"""
        return all(Crossword.is_word_filled(word) for word in self.words.values())

    def is_validly_filled(self, wordlist):
        """Returns whether the crossword is filled with words in the wordlist with no dupes"""
        if not self.is_filled():
            raise ValueError('not filled')
            return False  # some unfilled words
        if not all(word in wordlist.words for word in self.words.values()):
            raise ValueError('invalid words')
            return False  # some invalid words
        if not len(self.wordset) == len(self.words.values()):
            raise ValueError('dupes')
            return False  # some dupes
        if not all(
            self.fits_constraints(slot, self.words[slot], wordlist)
            for slot in self.slots
        ):
            raise ValueError('constraint violation')
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
    def from_grid(cls, grid, min_length=1):
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

        xw.__generate_slots_from_grid(min_length)

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

    def __generate_slots_from_grid(self, min_length=1):
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
                        if len(squares) >= min_length:
                            self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in row
            if word != '':
                if len(squares) >= min_length:
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
                        if len(squares) >= min_length:
                            self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in column
            if word != '':
                if len(squares) >= min_length:
                    self.add_slot(squares, word)

        self.generate_crossings()
