/**
 * @file word.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <string>

/**
 * Simple word class implementation.
 */
class Word {

    public:

        /**
         * Standard constructor implementation for Word class.
         */
        Word();

        /**
         * Custom constructor implementation for Word class.
         */
        Word(std::string characters);

        /**
         * Standard destructor implementation for Word class.
         */
        ~Word();

        /**
         * Returns whether there are any empty characters or spaces in the word object.
         */
        bool IsFilled();

        /**
         * Returns string containing the stored word.
         */
        std::string getWord();

    private:

        /**
         * Private member variable for use in the Word class.
         */
        std::string characters_;

};