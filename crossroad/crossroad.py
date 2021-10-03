import utils
import random

EMPTY = '·'
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
    def get_matches(self, pattern):
        # try to get from memo
        if pattern in self.pattern_matches:
            return self.pattern_matches[pattern]

        matches = []
        length = len(pattern)
        if length not in self.words_by_length:
            return []
        for w in self.words_by_length[length]:
            for i in range(length):
                if pattern[i] != EMPTY and pattern[i] != w[i]:
                    break
            else:
                matches.append(w)
        
        # write to memo
        self.pattern_matches[pattern] = matches
        return matches


# basic struct for a position in a grid where a word can go
class Slot:
    def __init__(self, row=0, col=0, dir=ACROSS):
        self.row = row
        self.col = col
        self.dir = dir

    def __hash__(self):
        return hash((self.row, self.col, self.dir))

    def __eq__(self, other):
        return (self.row, self.col, self.dir) == (other.row, other.col, other.dir)
    
    def __str__(self):
        return f'[{self.row}, {self.col}]-{self.dir}'


class Crossword:
    # fills grid of given size with empty squares
    def __init__(self, rows, cols, wordlist=None):
        self.rows = rows
        self.cols = cols
        self.wordlist = wordlist
        
        # initalize grid array
        self.grid = [[EMPTY for c in range(cols)] for r in range(rows)]
        
        # initialize words maps
        self.entries = {}
        self.across_crossings = {}
        self.down_crossings = {}

        self.generate_entries()

    # prints crossword
    def __str__(self):
        return '\n'.join([' '.join([letter for letter in row]) for row in self.grid])
    
    # returns whether given grid Slot contains a letter
    def is_letter(self, row, col):
        return self.grid[row][col] != EMPTY and self.grid[row][col] != BLOCK

    # places block in certain slot
    def put_block(self, row, col):
        self.grid[row][col] = BLOCK
        self.generate_entries()
    
    # sets character at index to given character
    def put_letter(self, slot, i, letter):
        entry = self.entries[slot]
        self.entries[slot] = entry[0:i] + letter + entry[i+1 :]
    
    # places word in given Slot
    def put_word(self, word, row=0, col=0, dir=ACROSS, add_to_wordlist=True):
        if add_to_wordlist and self.wordlist:
            self.wordlist.add_word(word)

        # place word in grid array
        if dir == DOWN:
            for y in range(len(word)):
                self.grid[row + y][col] = word[y]
        else:
            for x in range(len(word)):
                self.grid[row][col + x] = word[x]
        
        # place word in words map
        self.entries[Slot(row, col, dir)] = word

        # alter crossing words in words map
        if dir == DOWN:
            for y in range(len(word)):
                crossing_slot = self.across_crossings[row + y, col]
                self.put_letter(crossing_slot, col - crossing_slot.col, word[y])
        else:
            for x in range(len(word)):
                crossing_slot = self.down_crossings[row, col + x]
                self.put_letter(crossing_slot, row - crossing_slot.row, word[x])

    # generates dictionary that maps Slot to word
    def generate_entries(self):
        # reset words map
        self.entries = {}
        self.across_crossings = {}
        self.down_crossings = {}

        # generate across words
        for r in range(self.rows):
            curr_word = ''
            slot = Slot(0, 0, ACROSS)
            for c in range(self.cols):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    self.across_crossings[r, c] = slot
                    curr_word += letter
                    if len(curr_word) == 1:
                        slot.row = r
                        slot.col = c
                else:
                    if curr_word != '':
                        self.entries[slot] = curr_word
                        curr_word = ''
                        slot = Slot(0, 0, ACROSS)
            if curr_word != '':
                self.entries[slot] = curr_word

        # generate down words
        for c in range(self.cols):
            curr_word = ''
            slot = Slot(0, 0, DOWN)
            for r in range(self.rows):
                letter = self.grid[r][c]
                if letter != BLOCK:
                    self.down_crossings[r, c] = slot
                    curr_word += letter
                    if len(curr_word) == 1:
                        slot.row = r
                        slot.col = c
                else:
                    if curr_word != '':
                        self.entries[slot] = curr_word
                        curr_word = ''
                        slot = Slot(0, 0, DOWN)
            if curr_word != '':
                self.entries[slot] = curr_word

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
        for pos in self.entries:
            w = self.entries[pos]
            if self.is_filled(w) and w not in self.wordlist.words:
                return False
        return True

    # returns whether or not a given word is already in the grid
    # TODO: make more efficient with word set
    def is_dupe(self, word):
        for pos in self.entries:
            if self.entries[pos] == word:
                return True
        return False
    
    # fill the crossword using the given algorithm
    def fill(self, strategy, printout=False):
        if strategy == 'dfs':
            self.fill_dfs(printout)
        else:
            raise ValueError('Invalid strategy')
    
    # fills the crossword using a naive, terrible, dfs algorithm
    # TODO: optimize efficiency of this before moving onto heuristic-based algorithm
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
        random.shuffle(matches)

        for match in matches:
            if self.is_dupe(match):
                continue
            # try placing the match in slot and try to solve with the match there, otherwise continue
            self.put_word(match, slot.row, slot.col, slot.dir)
            if not self.has_valid_words():
                continue
            if self.fill_dfs(printout=printout):
                return True
        # if no match works, restore previous word
        self.put_word(previous_word, slot.row, slot.col, slot.dir, add_to_wordlist=False)
        return False