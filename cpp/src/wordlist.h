/**
 * @file wordlist.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <set>
#include <map>

#include "word.h"

/**
 * This class implements the general wordlist framework.
 * Collection of words to be used for filling a crossword.
 */
class Wordlist {

    public:

        /**
         * Standard constructor for general Wordlist class.
         */
        Wordlist();

        /**
         * Custom constructor for general Wordlist class.
         */
        Wordlist();

        /**
         * Standard destructor for general Wordlist class.
         */
        ~Wordlist();

    private:

        /**
         * 
         */
        std::set<Word> words_;

        

};

