/**
 * @file crossword.cpp
 * Jack Joshi, Adam Aaronson
 * February 2022
 */

#include "crossword.h"
#include <stdexcept>

/**
 * Standard constructor for general crossword class.
 */
Crossword::Crossword() {}

/**
 * Custom constructor for general crossword class.
 */
Crossword::Crossword(std::set<Slot> slots, std::map<Square*, std::map<Slot, int>> squares, std::map<Slot, Word> words, std::set<Word> wordset, Wordlist wordlist) {
    slots_ = slots;
    squares_ = squares;
    words_ = words;
    wordset_ = wordset;
}

/**
 * Standard destructor for general crossword class.
 */
~Crossword() {

    #warning "Update destructor to properly iterate through and delete map containing pointer to Squares"

}

std::ostream &operator<<(std::ostream &out, const Crossword &crossword)
{
    #warning "not implemented accurately yet"
    std::string out = "";
    for (Slot * slot : slots_) {
        out = out + ": " + words_[slot];
        for (Square * square : slot) {
            std::string square_char(1, square->GetLetter());
            out = out + square_char;
        }
        out = out + ", \n"
    }
    return out;
}

/**
 * Places given letter at ith square of given slot.
 * NOTE: Does not update crossing slots.
 */
void Crossword::PutLetter(Slot slot, int i, char letter) {

    old_word = words_[slot];
    if (i >= length(slot)) {
        throw std::invalid_argument("Index greater than word length!");
    }

    // no change
    if (old_word[i] == letter) {
        return;
    }

    new_word = old_word[0:i] + letter + old_word[i+1:];

    // update wordset
    if (wordset_.contains(old_word)) {
        wordset_.erase(old_word);
    }
    
    if (IsWordFilled(new_word)) {
        wordset_.insert(new_word);
    }

    // update words for just this slot, not crossing slots
    words_[slot] = new_word;

}

/**
 * Places word in given slot.
 * Defaults to adding the word to the wordlist if not already included.
 * Updates words in crossing slots using PutLetter().
 */
void Crossword::PutWord(Word word, Slot slot, Wordlist wordlist_to_update=NULL) {

    if (wordlist_to_update) {
        wordlist_to_update.AddWord(word);
    }

    prev_word = words_[slot];

    // place word in words map and wordset
    words_[slot] = word;
    if (IsWordFilled(prev_word)) {
        wordset_.erase(prev_word);
    }
    if (IsWordFilled(word)) {
        wordset_.insert(word);
    }

    // update crossing words
    int i = 0;
    for (Square * square : slot) {
        for (Slot * crossing_slot : squares_[square]) {
            if (crossing_slot == slot) {
                #warning "Inputted slot should be a pointer"
                continue
            }
            PutLetter(crossing_slot, squares_[square][crossing_slot], word[i])
        }
        i++;
    }

}

/**
 * Returns whether word is completely filled.
 */
bool Crossword::IsWordFilled(Word word) {
    return word.IsFilled();
}

/**
 * Returns whether word is a dupe (i.e. already in the wordset).
 */
bool Crossword::IsDupe(Word word) {
    return wordset_.contains(word);
}

/**
 * Returns whether every square in the grid is non-empty.
 */
bool Crossword::IsFilled() {
    for (std::map<Slot, Word>::iterator it = words_.begin(); it != words_.end(); ++it) {
        if (~IsWordFilled(it->second)) {
            return false;
        }
    }
    return true;
}

