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
~Word::Word() {}

/**
 * Returns whether there are any empty characters or spaces in the word object.
 */
Word::IsFilled() {
    for (char c : characters_) {
        if (c.isspace()) {
            return false;
        }
    }
    return true;
}