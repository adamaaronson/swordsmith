/**
 * @file crossword.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <set>
#include <map>
#include <string>

using namespace swordsmith;

/**
 * This class implements a general crossword framework.
 * The american crossword class is derived from this base class.
 */
class Crossword {

    public:

        /**
         * Standard constructor for general crossword class.
         */
        Crossword();

        /**
         * Custom constructor for general crossword class.
         */
        Crossword(std::set<Slot> slots, std::map<Square, std::map<Slot, int>> squares,
                  std::map<Slot, Word> words, std::set<Word> wordset, Wordlist wordlist);

        /**
         * Returns whether the given square contains a letter.
         */
        IsLetter(int row, int col);

        /**
         * Places given letter at ith square of given slot.
         * NOTE: Does not update crossing slots.
         */
        PutLetter(Slot slot, int i, char letter);

        /**
         * Places word in given slot.
         * Defaults to adding the word to the wordlist if not already included.
         * Updates words in crossing slots using PutLetter().
         */
        PutWord(Word word, Slot slot, bool add_to_wordlist=true);

        /**
         * Returns the unfilled slot in the grid with the fewest matches.
         * Also returns the corresponding number of matches.
         * Used as a next-slot heuristic.
         */
        FewestMatches();

        /**
         * Returns whether word is completely filled.
         */
        IsWordFilled(Word word);

        /**
         * Returns whether word is a dupe (i.e. already in the wordset).
         */
        IsDupe(Word word);

        /**
         * Returns whether every square in the frid is non-empty.
         */
        IsFilled();

        /**
         * Returns words that would cross the given slot if the given word was placed into it.
         * Does not actually place word in slot.
         * Used for Minlook() heuristic.
         */
        GetCrossingWords(Slot slot, Word word=NULL);

        /**
         * Randomly looks at k possible matches.
         * Returns index of match that yields maximum number of crossing words if placed in slot.
         * Also returns the indices of matches that immediately cause inconsistencies.
         * Determines number of crossing words by computing the sum of logarithms of crossing match counts.
         * Used for Minlook() and arc-consistency heuristic.
         */
        Minlook(Slot slot, int k, std::array<int> matches);

    private:

        /**
         * Set of slots in the crossword.
         */
        std::set<Slot> slots_;

        /**
         * Map of maps that keeps track of which slots contain which squares.
         * Maps from square to map, which maps from slot to index of square within slot.
         */
        std::map<Square, std::map<Slot, int>> squares_;

        /**
         * Maps each slot to its corresponding word.
         * Updated as grid is filled.
         */
        std::map<Slot, Word> words_;

        /**
         * Set of filled words in the grid.
         * Used for dupe detection.
         * Updated as grid is filled.
         */
        std::set<Word> wordset_;

        /**
         * Contains all of the crossword's filled words.
         */
        Wordlist wordlist_;

};
