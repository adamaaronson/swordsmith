/**
 * @file wordlist.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * March 2022
 */

#include <sqlite3.h>

#include "wordlist.h"

#warning "Should the stored private member variables be pointers?"

/**
 * Standard constructor for general Wordlist class.
 */
Wordlist::Wordlist() {}

/**
 * Custom constructor for general Wordlist class.
 */
Wordlist::Wordlist(std::set<Word> words) {
    words_ = words;
}

/**
 * Standard destructor for general Wordlist class.
 */
Wordlist::~Wordlist() {
    for (const auto &pair : words_by_length) {
        delete[] words_by_length.second;
    }
}

/**
 * Initialize the database.
 */
void Wordlist::initDatabase() {

    std::map<int, std::vector<Word>*> words_by_length;

    // sort words by length
    for (Word word : words_) {
        if (words_by_length[word.GetLength()] == NULL) {
            words_by_length[word.GetLength()] = new std::vector<Word>(word);
        } else {
            words_by_length[word.GetLength()].push_back(word);
        }
    }

    for (const auto &pair : words_by_length) {

        // initialize table for each length
        int length = pair.first;
        std::string table_name = getTableName(length);
        
        #warning "IMPLEMENTATION NOT FINISHED YET!"

    }

}

/**
 * Add word to wordlist.
 */
void Wordlist::addWord(Word word) {
    if (~words_.contains(word)) {
        words_.insert(word);
        added_words_.insert(word);
    }
}

/**
 * Remove word from wordlist.
 */
void Wordlist::removeWord(Word word) {
    if (words_.contains(word)) {
        words_.erase(word);
    }
    if (added_words_.contains(word)) {
        added_words_.erase(word);
    }
}

/**
 * Returns matches for the given pattern.
 */
std::vector<NULL> Wordlist::getMatches(std::string pattern) {

    #warning "IMPLEMENTATION NOT FINISHED YET"

}

/**
 * Returns the table name for SQLite.
 */
std::string Wordlist::getTableName(int length) {
    return "words" + std::to_string(length);
}

/**
 * Returns the column name for SQLite.
 */
std::string Wordlist::getColumnName(int index) {
    return "letter" + std::to_string(index);
}