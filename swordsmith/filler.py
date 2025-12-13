import math
import os
import time

from abc import ABC, abstractmethod
from random import shuffle

from crossword import Crossword


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        for crossing_slot, crossing_word in new_crossing_words:
            if not Crossword.is_word_filled(crossing_word):
                continue
            if crossing_word not in wordlist.words:
                return False  # created invalid word
            if not crossword.fits_constraint(crossing_slot, crossing_word):
                return False  # violated constraint
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
            clear_terminal()
            print(crossword)

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if crossword.is_filled():
            return crossword.is_validly_filled(wordlist)

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
            clear_terminal()
            print(crossword)

        # if the grid is filled, succeed if every word is valid and otherwise fail
        if crossword.is_filled():
            return crossword.is_validly_filled(wordlist), None

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
            if failed_slot and failed_slot not in crossword.crossings[slot]:
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

    def __init__(self, k=5):
        self.k = k

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            clear_terminal()
            print(crossword)

        # if the grid is filled, succeed
        if crossword.is_filled():
            return crossword.is_validly_filled(wordlist)

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

    def __init__(self, k=5):
        self.k = k

    def fill(self, crossword, wordlist, animate, retry_time=None):
        if retry_time and time.time() > retry_time:
            raise RetryException()

        if animate:
            clear_terminal()
            print(crossword)

        # if the grid is filled, succeed
        if crossword.is_filled():
            return crossword.is_validly_filled(wordlist), None

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
            if failed_slot and failed_slot not in crossword.crossings[slot]:
                # undo this word, keep backjumping
                crossword.put_word(previous_word, slot)
                return False, failed_slot

        # if no match works, restore previous word
        crossword.put_word(previous_word, slot)
        return False, slot
