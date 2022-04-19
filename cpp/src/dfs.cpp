/**
 * @file dfs.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include <dfs.h>

/**
 * Standard constructor implementation for DFS.
 */
DFS::DFS()  {}

/**
 * Custom constructor implementation for DFS.
 */
DFS::DFS(Crossword crossword, bool animate) {
    crossword_ = crossword;
    animate_ = animate;
}

/**
 * Fills the given crossword using some strategy.
 * Virtual function that must be implemented.
 */
bool DFS::Fill() {

    if (animate_) {
        #warning "clear terminal"
        #warning "print crossword"
    }

    // if the grid is filled, succeed if every word is valid and otherwise fail
    if (crossword_.IsGridFilled()) {
        return true;
    }

    // choose slot with fewest matches
    slot, num_matches = crossword_.FewestMatches();

    // if some slot has zero matches, fail
    if (num_matches == 0) {
        return false;
    }

    // iterate through all possible matches in the fewest-match slot
    previous_word = crossword_.entries[slot];
    matches = crossword_.wordlist.GetMatches(previous_word);

    // randomly shuffle matches
    #warning "shuffle matches"

    // loop through matches
    for (SomeClass match : matches) {
        #warning "add appropriate class above"

        #warning "try"
            crossword_.PutWord(match, slot);
        #warning "except Dupe and BadWord errors"
            continue

        if DFS::Fill(crossword_, animate_) {
            return true;
        }
    }

    // if no match works, restore previous word
    crossword_.PutWord(previous_word, slot, add_to_wordlist=false);
    return false;

}
