/**
 * @file crossword.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "crossword.h"

/**
 * Standard constructor for general crossword class.
 */
Crossword::Crossword();

/**
 * Custom constructor for general crossword class.
 */
Crossword::Crossword(std::set<Slot> slots, std::map<Square, std::map<Slot, int>> squares,
            std::map<Slot, Word> words, std::set<Word> wordset, Wordlist wordlist);

/**
 * Returns whether the given square contains a letter.
 */
bool Crossword::IsLetter(int row, int col);

/**
 * Places given letter at ith square of given slot.
 * NOTE: Does not update crossing slots.
 */
void Crossword::PutLetter(Slot slot, int i, char letter);

/**
 * Places word in given slot.
 * Defaults to adding the word to the wordlist if not already included.
 * Updates words in crossing slots using PutLetter().
 */
void Crossword::PutWord(Word word, Slot slot, bool add_to_wordlist=true);

/**
 * Returns the unfilled slot in the grid with the fewest matches.
 * Also returns the corresponding number of matches.
 * Used as a next-slot heuristic.
 */
Crossword::FewestMatches();

/**
 * Returns whether word is completely filled.
 */
Crossword::IsWordFilled(Word word);

/**
 * Returns whether word is a dupe (i.e. already in the wordset).
 */
Crossword::IsDupe(Word word);

/**
 * Returns whether every square in the frid is non-empty.
 */
Crossword::IsFilled();

/**
 * Returns words that would cross the given slot if the given word was placed into it.
 * Does not actually place word in slot.
 * Used for Minlook() heuristic.
 */
Crossword::GetCrossingWords(Slot slot, Word word=NULL);

/**
 * Randomly looks at k possible matches.
 * Returns index of match that yields maximum number of crossing words if placed in slot.
 * Also returns the indices of matches that immediately cause inconsistencies.
 * Determines number of crossing words by computing the sum of logarithms of crossing match counts.
 * Used for Minlook() and arc-consistency heuristic.
 */
Crossword::Minlook(Slot slot, int k, std::array<int> matches);