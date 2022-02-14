import utils

import sqlite3
import math

from abc import ABC, abstractmethod
from random import shuffle
from collections import namedtuple, defaultdict

EMPTY = '.'
BLOCK = '█'

ACROSS = 'A'
DOWN = 'D'

# collection of words to be used for filling a crossword
class Wordlist:
    def __init__(self, words, db=None):
        self.words = set(words)
        self.added_words = set()

        # mapping from wildcard patterns to lists of matching words, used for memoization
        self.pattern_matches = {}

        if db:
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()

    def __get_table_name(self, length):
        return 'words' + str(length)
    
    def __get_column_name(self, index):
        return 'letter' + str(index)
    
    def init_database(self):
        words_by_length = defaultdict(set)

        for word in self.words:
            words_by_length[len(word)].add(word)

        for length in words_by_length:
            # initialize table for each length
            table_name = self.__get_table_name(length)
            column_names = ['word'] + [self.__get_column_name(index) for index in range(length)]
            columns_str = ', '.join(column_names)
            
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})')
            
            # add one row for each word
            word_row = list((w, *tuple(w)) for w in words_by_length[length])
            values_str = ', '.join('?' for _ in range(length + 1))
            
            self.cur.executemany(f'INSERT INTO {table_name} VALUES ({values_str})', word_row)

            # create indices

            for column_name in column_names:
                index_name = table_name + column_name

                self.cur.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})')
    
    def add_word(self, word):
        if word not in self.words:
            self.words.add(word)
            self.added_words.add(word)
    
    def remove_word(self, word):
        if word in self.words:
            self.words.remove(word)
        if word in self.added_words:
            self.added_words.remove(word)
    
    def get_matches(self, pattern):
        if pattern in self.pattern_matches:
            return self.pattern_matches[pattern]

        table_name = self.__get_table_name(len(pattern))
        wheres = [f'{self.__get_column_name(i)} = \'{pattern[i]}\'' for i in range(len(pattern)) if pattern[i] != EMPTY]
        where_str = 'WHERE ' + ' AND '.join(wheres) if wheres else ''

        self.cur.execute(f'SELECT word FROM {table_name} {where_str}')

        matches = [row[0] for row in self.cur.fetchall()]

        self.pattern_matches[pattern] = matches

        return matches


# coordinate in a grid
Square = namedtuple('Square', ['coords', 'letter'])

# position in a grid where a word can go
Slot = namedtuple('Slot', ['squares', 'word'])

# exception for when a duplicate entry is found
class DupeError(Exception):
    def __init__(self, message='Dupe found!'):
        self.message = message

# exception for when an invalid word is created
class BadWordError(Exception):
    def __init__(self, message='Not a word!'):
        self.message = message


class Crossword:
    # fills grid of given size with empty squares
    def __init__(self, wordlist=None):
        self.wordlist = wordlist
        
        self.slots = set()                                      # set of slots in the puzzle
        self.squares = defaultdict(lambda: defaultdict(int))    # square => slots that contain it => index of square in slot
        self.wordset = set()                                    # set of filled entries in puzzle
    
    # sets character at index to given character
    def put_letter(self, slot, i, letter):
        old_entry = self.entries[slot]
        if i >= len(old_entry):
            raise IndexError('Index greater than word length!')

        if old_entry[i] == letter:
            # no change
            return
        
        new_entry = old_entry[0:i] + letter + old_entry[i+1 :]

        # update entryset
        if old_entry in self.wordset:
            self.wordset.remove(old_entry)
        if self.is_filled(new_entry):
            if self.is_dupe(new_entry):
                raise DupeError()
            self.wordset.add(new_entry)
        
        self.entries[slot] = new_entry
    
    # places word in given Slot
    def put_word(self, word, slot, add_to_wordlist=True):
        row, col, dir = slot

        if add_to_wordlist and self.wordlist:
            self.wordlist.add_word(word)
        
        # check if dupe
        if self.is_dupe(word):
            raise DupeError()

        # place word in grid array
        if dir == DOWN:
            for y in range(len(word)):
                self.grid[row + y][col] = word[y]
        else:
            for x in range(len(word)):
                self.grid[row][col + x] = word[x]
        
        prev_word = self.entries[slot]
        
        # place word in entries map and entryset
        self.entries[slot] = word
        if self.is_filled(prev_word):
            self.wordset.remove(prev_word)
        if self.is_filled(word):
            self.wordset.add(word)
        
        # update crossing words
        for square in self.squares_in_slot[slot]:
            square_row, square_col = square
            if dir == DOWN:
                crossing_slot = self.across_slots[square]
                self.put_letter(crossing_slot, col - crossing_slot.col, self.grid[square_row][square_col])
            else:
                crossing_slot = self.down_slots[square]
                self.put_letter(crossing_slot, row - crossing_slot.row, self.grid[square_row][square_col])
            
            # check to see if it created an invalid crossing word
            crossing_word = self.entries[crossing_slot]
            
            if self.is_filled(crossing_word) and crossing_word not in self.wordlist.words:
                raise BadWordError()

    # prints the whole word map, nicely formatted
    def __str__(self):
        return '\n'.join(', '.join(str(s.coords) for s in s.squares) + ' ' + s.word for s in self.slots)
    
    # finds the slot that has the fewest possible matches, this is probably the best next place to look
    def fewest_matches(self):
        fewest_matches_slot = None
        fewest_matches = len(self.wordlist.words) + 1

        for slot in self.entries:
            word = self.entries[slot]
            if self.is_filled(word):
                continue
            matches = len(self.wordlist.get_matches(word))
            if matches < fewest_matches:
                fewest_matches = matches
                fewest_matches_slot = slot
        return fewest_matches_slot, fewest_matches
    
    # returns whether word is completely filled
    def is_filled(self, word):
        return EMPTY not in word

    # returns whether or not the whole crossword is filled
    def is_grid_filled(self):
        for row in self.grid:
            for letter in row:
                if letter == EMPTY:
                    return False
        return True

    # returns whether or not the crossword is validly filled
    def has_valid_words(self):
        for word in self.entries.values():
            if self.is_filled(word) and word not in self.wordlist.words:
                return False
        return True

    # returns whether or not a given word is already in the grid
    def is_dupe(self, word):
        return word in self.wordset

    # returns list of entries that cross the given slot, optionally given a word to theoretically be in the slot
    def get_crossing_entries(self, slot, word=None):
        if not word:
            word = self.entries[slot]
        
        crossing_entries = []

        for i, square in enumerate(self.squares_in_slot[slot]):
            letter = word[i]

            if slot.dir == DOWN:
                crossing_slot = self.across_slots[square]
                index = slot.col - crossing_slot.col
            else:
                crossing_slot = self.down_slots[square]
                index = slot.row - crossing_slot.row
            
            crossing_entry = self.entries[crossing_slot]
            crossing_entry = crossing_entry[:index] + letter + crossing_entry[index + 1:]

            crossing_entries.append(crossing_entry)
        
        return crossing_entries
    
    # considers given matches, returns index of the one that offers the most possible crossing entries
    # if none of them work, return -1
    def minlook(self, slot, k, matches):
        match_indices = range(min(k, len(matches))) # just take first k matches
        failed_indices = set()

        best_match_index = -1
        best_cross_product = -1

        for match_index in match_indices:
            cross_product = 0

            for crossing_entry in self.get_crossing_entries(slot, matches[match_index]):
                num_matches = len(self.wordlist.get_matches(crossing_entry))
                
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

class AmericanCrossword(Crossword):
    def __init__(self, rows, cols, wordlist=None):
        Crossword.__init__(self, wordlist)

        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for c in range(cols)] for r in range(rows)] # 2D array of squares

        self.generate_slots()

    # takes in array of chars and returns a crossword
    @classmethod
    def from_grid(cls, grid, wordlist=None):
        rows = len(grid)
        cols = len(grid[0])

        blocks = []
        
        for r in range(rows):
            blocks += [(r, c) for c in range(cols) if grid[r][c] == BLOCK]

        xw = cls(rows, cols, wordlist)
        if blocks:
            xw.put_blocks(blocks)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != BLOCK and grid[r][c] != EMPTY:
                    xw.grid[r][c] = grid[r][c]
        
        xw.generate_slots()

        return xw
    
    # prints crossword
    def __str__(self):
        return '\n'.join(', '.join(str(square.coords) for square in slot.squares) + ': ' + slot.word for slot in self.slots)
        return '\n'.join(' '.join([letter for letter in row]) for row in self.grid)

    # places block in certain square
    def put_block(self, row, col):
        self.grid[row][col] = BLOCK
        self.generate_slots()
    
    # places list of blocks in specified squares
    def put_blocks(self, coords):
        for row, col in coords:
            self.grid[row][col] = BLOCK
        self.generate_slots()
    
    def add_slot(self, squares, word):
        slot = Slot(tuple(squares), word)
        self.slots.add(slot)

        for i, square in enumerate(squares):
            self.squares[square][slot] = i
        
        if self.is_filled(word):
            self.wordset.add(word)

    def generate_slots(self):
        # reset slot mappings
        self.squares.clear()
        self.slots.clear()
        self.wordset.clear()

        # generate across words
        for r in range(self.rows):
            word = ''
            squares = []
            for c in range(self.cols):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    # add a letter to the current word
                    word += letter
                    squares.append(Square((r, c), letter))
                else:
                    # block hit, check to see if there's a word in progress
                    if word != '':
                        self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in row
            if word != '':
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
                    squares.append(Square((r, c), letter))
                else:
                    # block hit, check to see if there's a word in progress
                    if word != '':
                        self.add_slot(squares, word)
                        word = ''
                        squares = []
            # last word in column
            if word != '':
                self.add_slot(squares, word)


class Filler(ABC):
    @abstractmethod
    def fill(self, crossword, animate):
        """Fills the given crossword using some strategy."""

class DFSFiller(Filler):
    """Fills the crossword using a naive DFS algorithm:
    
    - keeps selecting unfilled slot with fewest possible matches
    - randomly chooses matching entry for that slot
    - backtracks if there is a slot with no matches"""

    def fill(self, crossword, animate):
        if animate:
            utils.clear_terminal()
            print(crossword)

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if crossword.is_grid_filled():
            return True

        # choose slot with fewest matches
        slot, num_matches = crossword.fewest_matches()

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False
        
        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.entries[slot]
        matches = crossword.wordlist.get_matches(crossword.entries[slot])

        # randomly shuffle matches
        shuffle(matches)

        for match in matches:
            # try placing the match in slot and try to solve with the match there, otherwise continue
            try:
                crossword.put_word(match, slot)
            except (DupeError, BadWordError):
                continue

            if self.fill(crossword, animate):
                return True
        # if no match works, restore previous word
        crossword.put_word(previous_word, slot, add_to_wordlist=False)
        return False

    
class MinlookFiller(Filler):
    """# fills the crossword using a dfs algorithm with minlook heuristic:
    # - keeps selecting unfilled slot with fewest possible matches
    # - considers k random matching word, chooses word with the most possible crossing entries (product of # in each slot)
    # - backtracks if there is a slot with no matches"""
    
    def __init__(self, k):
        self.k = k

    def fill(self, crossword, animate):
        if animate:
            utils.clear_terminal()
            print(crossword)
        
        # if the grid is filled, succeed
        if crossword.is_grid_filled():
            return True

        # choose slot with fewest matches
        slot, num_matches = crossword.fewest_matches()

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False
        
        # iterate through all possible matches in the fewest-match slot
        previous_word = crossword.entries[slot]
        matches = crossword.wordlist.get_matches(crossword.entries[slot])

        # randomly shuffle matches
        shuffle(matches)

        while matches:
            match_index, failed_indices = crossword.minlook(slot, self.k, matches)

            if match_index != -1:
                match = matches[match_index]
            
            # remove failed matches and chosen match
            matches = [matches[i] for i in range(len(matches)) if i != match_index and i not in failed_indices]
            
            # if no matches were found, try another batch if possible
            if match_index == -1:
                continue

            # try placing the match in slot and try to solve with the match there, otherwise continue
            try:
                crossword.put_word(match, slot)
            except (DupeError, BadWordError):
                continue
            
            if self.fill(crossword, animate):
                return True
        # if no match works, restore previous word
        crossword.put_word(previous_word, slot, add_to_wordlist=False)
        return False