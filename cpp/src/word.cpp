/**
 * @file word.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "word.h"

/**
 * Standard constructor implementation for Word class.
 */
Word::Word() {}

/**
 * Custom constructor implementation for Word class.
 */
Word::Word(std::string characters) {
    characters_ = characters;
}

/**
 * Standard destructor implementation for Word class.
 */
Word::~Word() {}

/**
 * Returns whether there are any empty characters or spaces in the word object.
 */
bool Word::IsFilled() {

    // if the word does not exist yet, return false
    if (characters_.length() == 0) {return false;}

    // if an empty character or space is detected, return false
    for (int i = 0; i < characters_.length(); i++) {
        char c = characters_[i];
        if (isspace(c)) {
            return false;
        }
    }

    // else, return true
    return true;

}

/**
 * Returns string containing the stored word.
 */
std::string Word::GetWord() {
    return characters_;
}