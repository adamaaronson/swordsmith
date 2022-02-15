/**
 * @file filler.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

using namespace swordsmith;

/**
 * This is a base class for algorithms to fill crossword grids.
 * DFS and Minlook will inherit from this base class.
 */
class Filler {
    public:
        bool fill(Crossword crossword, bool animate);

    private:
        Crossword crossword_;
        bool animate_;
};