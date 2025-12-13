from collections import defaultdict
import re

from constants import EMPTY


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
