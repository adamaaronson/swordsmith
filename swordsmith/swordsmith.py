import utils
import math

from random import shuffle
from collections import namedtuple, defaultdict

EMPTY = '.'
BLOCK = '█'

ACROSS = 'A'
DOWN = 'D'

# collection of words to be used for filling a crossword
class Wordlist:
    def __init__(self, words):
        self.words = set(words)
        self.added_words = set()

        # mapping from lengths to sets of words of that length
        self.words_by_length = {}
        for w in words:
            self.__add_to_words_by_length(w)

        # mapping from wildcard patterns to lists of matching words, used for memoization
        self.pattern_matches = {}
    
    def add_word(self, word):
        if word not in self.words:
            self.words.add(word)
            self.added_words.add(word)
            self.__add_to_words_by_length(word)
    
    def remove_word(self, word):
        if word in self.words:
            self.words.remove(word)
            self.__remove_from_words_by_length(word)
        if word in self.added_words:
            self.added_words.remove(word)
    
    def __add_to_words_by_length(self, word):
        length = len(word)
        if length in self.words_by_length:
            self.words_by_length[length].add(word)
        else:
            self.words_by_length[length] = set([word])
    
    def __remove_from_words_by_length(self, word):
        length = len(word)
        if length in self.words_by_length:
            if word in self.words_by_length[length]:
                self.words_by_length[length].remove(word)
    
    # return words in wordlist that match the pattern of this word
    # TODO: look into table indexing to match each character of the word, something something sqlite
    def get_matches(self, pattern):
        # try to get from memo
        if pattern in self.pattern_matches:
            return self.pattern_matches[pattern]
        
        matches = []
        length = len(pattern)
        if length not in self.words_by_length:
            return []
        
        # leverage a previously searched superpattern if possible,
        # e.g. if the pattern is A??M we might have already searched for A??? or ???M
        candidates = self.words_by_length[length]
        for i in range(len(pattern)):
            if pattern[i] == EMPTY:
                continue
            superpattern = pattern[:i] + EMPTY + pattern[i+1:]
            if superpattern in self.pattern_matches:
                candidates = self.pattern_matches[superpattern]
                break
        
        for w in candidates:
            for i in range(length):
                if pattern[i] != EMPTY and pattern[i] != w[i]:
                    break
            else:
                matches.append(w)
        
        # write to memo
        self.pattern_matches[pattern] = matches
        return matches

# position in a grid where a word can go
Square = namedtuple('Square', ['row', 'col'])
Slot = namedtuple('Slot', ['row', 'col', 'dir'])

# exception for when a duplicate entry is found
class DupeError(Exception):
    def __init__(self, message='Dupe found!'):
        self.message = message

# exception for when an invalid word is created
class BadWordError(Exception):
    def __init__(self, message='Not a word!'):
        self.message = message

class InvalidStrategyError(Exception):
    def __init__(self, message='Invalid strategy!'):
        self.message = message

class Crossword:
    # fills grid of given size with empty squares
    def __init__(self, rows, cols, wordlist=None):
        self.rows = rows
        self.cols = cols
        self.wordlist = wordlist
        
        self.grid = [[EMPTY for c in range(cols)] for r in range(rows)] # 2D array of squares
        
        self.entries = {}               # slot => entry it contains
        self.entryset = set()           # set of filled entries in puzzle

        self.across_slots = {}          # square => across slot that contains it
        self.down_slots = {}            # square => down slot that contains it
        
        self.squares_in_slot = defaultdict(list)         # slot => list of squares it contains     
        self.slots_crossing_slot = defaultdict(set)      # slot => set of slots it crosses

        self.generate_slots()
    
    # prints crossword
    def __str__(self):
        return '\n'.join([' '.join([letter for letter in row]) for row in self.grid])
    
    # takes in boolean array and returns a crossword where True = block and False = empty
    @classmethod
    def from_grid(cls, grid, wordlist=None):
        rows = len(grid)
        cols = len(grid[0])

        blocks = sum([[(r, c) for c in range(cols) if grid[r][c]] for r in range(rows)], [])

        xw = cls(rows, cols, wordlist)
        xw.put_blocks(blocks)

        return xw

    # returns whether given grid Slot contains a letter
    def is_letter(self, row, col):
        return self.grid[row][col] != EMPTY and self.grid[row][col] != BLOCK

    # places block in certain slot
    def put_block(self, row, col):
        self.grid[row][col] = BLOCK
        self.generate_slots()
    
    # places list of blocks in specified slots
    def put_blocks(self, coords):
        for row, col in coords:
            self.grid[row][col] = BLOCK
        self.generate_slots()
    
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
        if old_entry in self.entryset:
            self.entryset.remove(old_entry)
        if self.is_filled(new_entry):
            if self.is_dupe(new_entry):
                raise DupeError()
            self.entryset.add(new_entry)
        
        self.entries[slot] = new_entry
    
    # places word in given Slot
    def put_word(self, word, row=0, col=0, dir=ACROSS, add_to_wordlist=True):
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
        
        slot = Slot(row, col, dir)
        prev_word = self.entries[slot]
        
        # place word in entries map and entryset
        self.entries[slot] = word
        if self.is_filled(prev_word):
            self.entryset.remove(prev_word)
        if self.is_filled(word):
            self.entryset.add(word)
        
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
                

    # generates dictionary that maps Slot to word
    def generate_slots(self):
        # reset slot mappings
        self.entries.clear()
        self.across_slots.clear()
        self.down_slots.clear()
        self.squares_in_slot.clear()
        self.slots_crossing_slot.clear()

        # generate across words
        for r in range(self.rows):
            curr_word = ''
            slot = Slot(0, 0, ACROSS)
            for c in range(self.cols):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    # add a letter to the current word
                    curr_word += letter
                    if len(curr_word) == 1:
                        slot = Slot(r, c, ACROSS)
                    self.across_slots[r, c] = slot
                    self.squares_in_slot[slot].append((r, c))
                else:
                    # block hit, check to see if there's a word in progress
                    if curr_word != '':
                        self.entries[slot] = curr_word
                        curr_word = ''
                        slot = None
            # last word in row
            if curr_word != '':
                self.entries[slot] = curr_word

        # generate down words
        for c in range(self.cols):
            curr_word = ''
            slot = Slot(0, 0, DOWN)
            for r in range(self.rows):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    # add a letter to the current word
                    curr_word += letter
                    if len(curr_word) == 1:
                        slot = Slot(r, c, DOWN)
                    self.down_slots[r, c] = slot
                    self.squares_in_slot[slot].append((r, c))
                else:
                    # block hit, check to see if there's a word in progress
                    if curr_word != '':
                        self.entries[slot] = curr_word
                        curr_word = ''
                        slot = None
            # last word in column
            if curr_word != '':
                self.entries[slot] = curr_word
        
        # determine crossing slots
        for square in self.across_slots:
            if square in self.down_slots:
                across_slot = self.across_slots[square]
                down_slot = self.down_slots[square]
                self.slots_crossing_slot[across_slot].add(down_slot)
                self.slots_crossing_slot[down_slot].add(across_slot)

    # prints the whole word map, nicely formatted
    def print_words(self):
        for slot in self.entries:
            print(slot.row, slot.col, slot.dir, self.entries[slot])

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
        return (fewest_matches_slot, fewest_matches)
    
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
        return word in self.entryset

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

    
    # fill the crossword using the given algorithm
    def fill(self, strategy, k=10, printout=False):
        if strategy == 'dfs':
            self.fill_dfs(printout)
        elif strategy == 'minlook':
            self.fill_minlook(k, printout=printout)
        else:
            raise InvalidStrategyError()
    
    # fills the crossword using a naive dfs algorithm:
    # - keeps selecting unfilled slot with fewest possible matches
    # - randomly chooses matching entry for that slot
    # - backtracks if there is a slot with no matches
    def fill_dfs(self, printout=False):
        if printout:
            utils.clear_terminal()
            print(self)

        # choose slot with fewest matches
        slot, num_matches = self.fewest_matches()

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if self.is_grid_filled():
            return self.has_valid_words()
        
        # iterate through all possible matches in the fewest-match slot
        previous_word = self.entries[slot]
        matches = self.wordlist.get_matches(self.entries[slot])

        # randomly shuffle matches, this miiiight be slow
        shuffle(matches)

        for match in matches:
            # try placing the match in slot and try to solve with the match there, otherwise continue
            try:
                self.put_word(match, *slot)
            except (DupeError, BadWordError):
                continue

            if self.fill_dfs(printout=printout):
                return True
        # if no match works, restore previous word
        self.put_word(previous_word, *slot, add_to_wordlist=False)
        return False
    
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

    
    # fills the crossword using a dfs algorithm with minlook heuristic:
    # - keeps selecting unfilled slot with fewest possible matches
    # - considers k random matching word, chooses word with the most possible crossing entries (product of # in each slot)
    # - backtracks if there is a slot with no matches
    def fill_minlook(self, k, printout=False):
        if printout:
            utils.clear_terminal()
            print(self)

        # choose slot with fewest matches
        slot, num_matches = self.fewest_matches()

        # if some slot has zero matches, fail
        if num_matches == 0:
            return False

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if self.is_grid_filled():
            return self.has_valid_words()
        
        # iterate through all possible matches in the fewest-match slot
        previous_word = self.entries[slot]
        matches = self.wordlist.get_matches(self.entries[slot])

        # randomly shuffle matches, this miiiight be slow
        shuffle(matches)

        while matches:
            match_index, failed_indices = self.minlook(slot, k, matches)

            if match_index != -1:
                match = matches[match_index]
            
            # remove failed matches and chosen match
            matches = [matches[i] for i in range(len(matches)) if i != match_index and i not in failed_indices]
            
            # if no matches were found, try another batch if possible
            if match_index == -1:
                continue

            # try placing the match in slot and try to solve with the match there, otherwise continue
            try:
                self.put_word(match, *slot)
            except (DupeError, BadWordError):
                continue
            
            if self.fill_minlook(k, printout):
                return True
        # if no match works, restore previous word
        self.put_word(previous_word, *slot, add_to_wordlist=False)
        return False