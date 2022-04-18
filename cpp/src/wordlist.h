/**
 * @file wordlist.h
 * Jack Joshi, Adam Aaronson
 * March 2022
 */

#pragma once

#include <set>
#include <map>
#include <vector>

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
        Wordlist(std::set<Word> words);

        /**
         * Standard destructor for general Wordlist class.
         */
        ~Wordlist();

        /**
         * Initialize the database.
         */
        void initDatabase();

        /**
         * Add word to wordlist.
         */
        void addWord(Word word);

        /**
         * Remove word from wordlist.
         */
        void removeWord(Word word);

        /**
         * Returns matches for the given pattern.
         */
        std::vector<NULL> getMatches(std::string pattern);


    private:

        /**
         * Set of all words in the wordlist.
         */
        std::set<Word> words_;

        /**
         * Set of words added to the wordlist.
         */
        std::set<Word> added_words_;

        /**
         * Map from pattern to matches.
         */
        std::map<std::string, std::vector<NULL>> pattern_matches_;

        /**
         * Returns the table name for SQLite.
         */
        std::string getTableName(int length);

        /**
         * Returns the column name for SQLite.
         */
        std::string getColumnName(int index);

};

