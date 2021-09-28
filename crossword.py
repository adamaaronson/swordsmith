import os
from random import shuffle

class Position:
    ACROSS = 'across'
    DOWN = 'down'

    def __init__(self, row=0, col=0, dir=ACROSS):
        self.row = row
        self.col = col
        self.dir = dir

    def __hash__(self):
        return hash((self.row, self.col, self.dir))

    def __eq__(self, other):
        return (self.row, self.col, self.dir) == (other.row, other.col, other.dir)

class Word:
    def __init__(self, word):
        self.word = word
    
    def __str__(self):
        return self.word

    def __hash__(self):
        return hash((self.word))

    def __eq__(self, other):
        return self.word == other.word

    # return words in wordlist that match the pattern of this word
    # TODO: optimize this with a trie or regex or something
    def get_matches(self, wordlist):
        matches = []
        length = len(self.word)
        for w in wordlist:
            if len(w) == length:
                for i in range(length):
                    if self.word[i] != Crossword.EMPTY and self.word[i] != w[i]:
                        break
                else:
                    matches.append(w)
        return matches
    
    # returns number of words in wordlist that match pattern of this word
    def num_matches(self, wordlist):
        matches = 0
        length = len(self.word)
        for w in [w.upper() for w in wordlist if len(w) == length]:
            for i in range(length):
                if self.word[i] != Crossword.EMPTY and self.word[i] != w[i]:
                    break
            else:
                matches += 1
        return matches

    # returns whether word is completely filled
    def is_filled(self):
        for l in self.word:
            if l == Crossword.EMPTY:
                return False
        return True

    # sets character at index to given character
    def set_letter_at_index(self, letter, i):
        self.word = self.word[0:i] + letter + self.word[i+1 :]

class Crossword:
    EMPTY = '.'
    BLOCK = '#'

    # fills grid of given size with empty squares
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # initalize grid array
        self.grid = []
        for _ in range(rows):
            self.grid.append([])
            for _ in range(cols):
                self.grid[len(self.grid) - 1].append(Crossword.EMPTY)
        
        # initialize words map
        self.words = {}
        self.generate_words()

    # prints crossword
    def __str__(self):
        output = ''
        for row in self.grid:
            for letter in row:
                output += letter
            output += '\n'
        return output

    # returns whether given grid Position contains a letter
    def is_letter(self, row, col):
        return self.grid[row][col] != Crossword.EMPTY and self.grid[row][col] != Crossword.BLOCK
    
    # places word in given Position
    def put_word(self, word, row=0, col=0, dir=Position.ACROSS):
        # place word in grid array
        if dir == Position.DOWN:
            for y in range(len(word)):
                self.grid[row + y][col] = word[y]
        else:
            for x in range(len(word)):
                self.grid[row][col + x] = word[x]
        
        # place word in words map
        self.words[Position(row, col, dir)] = Word(word)

        # alter crossing words in words map
        if dir == Position.DOWN:
            for y in range(len(word)):
                x = col
                while Position(row + y, x, Position.ACROSS) not in self.words:
                    x -= 1
                self.words[Position(row + y, x, Position.ACROSS)].set_letter_at_index(word[y], col - x)
        else:
            for x in range(len(word)):
                y = row
                while Position(y, col + x, Position.DOWN) not in self.words:
                    y -= 1
                self.words[Position(y, col + x, Position.DOWN)].set_letter_at_index(word[x], row - y)
    
    # places block in certain position
    def put_block(self, row, col):
        self.grid[row][col] = Crossword.BLOCK
        self.generate_words()

    # generates dictionary that maps Position to Word
    def generate_words(self):
        # reset words map
        self.words = {}

        # generate across words
        for r in range(self.rows):
            curr_word = ''
            position = Position(0, 0, Position.ACROSS)
            for c in range(self.cols):
                letter = self.grid[r][c]
                if letter != Crossword.BLOCK:
                    curr_word += letter
                    if len(curr_word) == 1:
                        position.row = r
                        position.col = c
                else:
                    if curr_word != '':
                        self.words[position] = Word(curr_word)
                        curr_word = ''
                        position = Position(0, 0, Position.ACROSS)
            if curr_word != '':
                self.words[position] = Word(curr_word)

        # generate down words
        for c in range(self.cols):
            curr_word = ''
            position = Position(0, 0, Position.DOWN)
            for r in range(self.rows):
                letter = self.grid[r][c]
                if letter != Crossword.BLOCK:
                    curr_word += letter
                    if len(curr_word) == 1:
                        position.row = r
                        position.col = c
                else:
                    if curr_word != '':
                        self.words[position] = Word(curr_word)
                        curr_word = ''
                        position = Position(0, 0, Position.DOWN)
            if curr_word != '':
                self.words[position] = Word(curr_word)

    # prints the whole word map, nicely formatted
    def print_words(self):
        for position in self.words:
            print(position.row, position.col, position.dir, self.words[position])

    # finds the position that has the fewest possible matches, this is probably the best next place to look
    def fewest_matches(self, wordlist):
        fewest_matches_position = None
        fewest_matches = len(wordlist) + 1

        for position in self.words:
            word = self.words[position]
            if word.is_filled():
                continue
            matches = word.num_matches(wordlist)
            if matches < fewest_matches:
                fewest_matches = matches
                fewest_matches_position = position
        return (fewest_matches_position, fewest_matches)

    # returns whether or not the whole crossword is filled
    def is_filled(self):
        for row in self.grid:
            for letter in row:
                if letter == Crossword.EMPTY:
                    return False
        return True

    # returns whether or not the crossword is validly filled
    def has_valid_words(self, wordlist):
        for pos in self.words:
            w = self.words[pos]
            if w.is_filled() and w.word not in wordlist:
                return False
        return True

    # returns whether or not a given word is already in the grid
    def is_dupe(self, word):
        for pos in self.words:
            if self.words[pos].word == word:
                return True
        return False


    def solve(self, wordlist):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)

        # choose position with fewest matches
        fm = self.fewest_matches(wordlist)
        position = fm[0]
        num_matches = fm[1]

        # if some position has zero matches, fail
        if num_matches == 0:
            return False

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if self.is_filled():
            return self.has_valid_words(wordlist)
        else:
            # iterate through all possible matches in the fewest-match position
            previous_word = self.words[position]
            matches = self.words[position].get_matches(wordlist)
            for match in matches:
                if self.is_dupe(match):
                    continue
                # try placing the match in position and try to solve with the match there, otherwise continue
                self.put_word(match, position.row, position.col, position.dir)
                if not self.has_valid_words(wordlist):
                    continue
                if self.solve(wordlist):
                    return True
            # if no match works, restore previous word
            self.put_word(previous_word.word, position.row, position.col, position.dir)
            return False

size = 7

wordlist = [w.upper() for w in open('allwords.txt').read().splitlines() if len(w) <= size]
shuffle(wordlist)

xword = Crossword(size, size)

xword.put_block(0,0)
xword.put_block(6,6)

# xword.put_block(0,4)
# xword.put_block(1,4)
# xword.put_block(2,4)
# xword.put_block(6,4)
# xword.put_block(7,4)
# xword.put_block(8,4)
# xword.put_block(4,0)
# xword.put_block(4,1)
# xword.put_block(4,2)
# xword.put_block(4,6)
# xword.put_block(4,7)
# xword.put_block(4,8)

xword.solve(wordlist)