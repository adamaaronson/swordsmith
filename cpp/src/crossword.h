/**
 * @file crossword.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <set>
#include <map>
#include <string>
#include <vector>
#include <tuple>
#include <ostream>

#include "square.h"
#include "word.h"
#include "slot.h"

/**
 * This class implements a general crossword framework.
 * The american crossword class is derived from this base class.
 */
class Crossword {

    public:

        /**
         * Standard constructor for general Crossword class.
         */
        Crossword();

        /**
         * Custom constructor for general Crossword class.
         */
        Crossword(std::set<Slot> slots, std::map<Square, std::map<Slot, int>> squares,
                  std::map<Slot, Word> words, std::set<Word> wordset, Wordlist wordlist);

        /**
         * Standard destructor for general Crossword class.
         */
        ~Crossword();

        /**
         * Places given letter at ith square of given slot.
         * NOTE: Does not update crossing slots.
         */
        void PutLetter(Slot slot, int i, char letter);

        /**
         * Places word in given slot.
         * Defaults to adding the word to the wordlist if not already included.
         * Updates words in crossing slots using PutLetter().
         */
        void PutWord(Word word, Slot slot, bool wordlist_to_update=NULL);

        /**
         * Returns whether word is completely filled.
         */
        bool IsWordFilled(Word word);

        /**
         * Returns whether word is a dupe (i.e. already in the wordset).
         */
        bool IsDupe(Word word);

        /**
         * Returns whether every square in the grid is non-empty.
         */
        bool IsFilled();

        /**
         * Returns words that would cross the given slot if the given word was placed into it.
         * Does not actually place word in slot.
         * Used for Minlook() heuristic.
         */
        std::vector<std::string> GetCrossingWords(Slot slot, Word word=NULL);

        /**
         * Randomly looks at k possible matches.
         * Returns index of match that yields maximum number of crossing words if placed in slot.
         * Also returns the indices of matches that immediately cause inconsistencies.
         * Determines number of crossing words by computing the sum of logarithms of crossing match counts.
         * Used for Minlook() and arc-consistency heuristic.
         */
        std::tuple<int, std::vector<int>> Minlook(Slot slot, int k, std::vector<int> matches);

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

};

#warning "Not sure if this is where the operator override should be"
std::ostream &operator<<(std::ostream &out, const Crossword &crossword);
