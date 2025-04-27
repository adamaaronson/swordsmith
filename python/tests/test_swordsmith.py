import sys
import unittest

sys.path.append('../swordsmith')

import swordsmith as sw

GRID_5x = '../swordsmith/grid/5x.txt'
GRID_15x = '../swordsmith/grid/15xcommon.txt'
WORDLIST = '../swordsmith/wordlist/spreadthewordlist.dict'

class Test5xDFS(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_5x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.DFSFiller()

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test5xDFSBackjump(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_5x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.DFSBackjumpFiller()

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test5xMinlook(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_5x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.MinlookFiller(5)

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test5xMinlookBackjump(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_5x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.MinlookBackjumpFiller(5)

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test15xDFS(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_15x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.DFSFiller()

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test15xDFSBackjump(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_15x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.DFSBackjumpFiller()

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test15xMinlook(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_15x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.MinlookFiller(5)

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

class Test15xMinlookBackjump(unittest.TestCase):
    def runTest(self):
        grid = sw.read_grid(GRID_15x)
        crossword = sw.AmericanCrossword.from_grid(grid)
        wordlist = sw.read_wordlist(WORDLIST)
        filler = sw.MinlookBackjumpFiller(5)

        filler.fill(crossword, wordlist, animate=False)
        self.assertTrue(crossword.is_validly_filled(wordlist))

unittest.main()