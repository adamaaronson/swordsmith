/**
 * @file dfs.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include "filler.h"

using namespace swordsmith;

/**
 * This class implements a DFS approach for filling crossword grids.
 * DFS is derived from the Filler class.
 */
class DFS : public Filler {

    public:

        /**
         * Standard constructor implementation for DFS.
         */
        DFS();

        /**
         * Custom constructor implementation for DFS.
         */
        DFS(Crossword crossword, bool animate);

        /**
         * Fills the given crossword using some strategy.
         * Virtual function that must be implemented.
         */
        bool Fill(Crossword crossword, bool animate);

    private:

        /**
         * Private member variables for use in the DFS class.
         */
        Crossword crossword_;
        bool animate_;

};
