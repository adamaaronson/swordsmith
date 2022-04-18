/**
 * @file american_crossword.h
 * Jack Joshi, Adam Aaronson
 * February 2022
 */

#pragma once

#include <vector>
#include <tuple>
#include <map>
#include <set>

#include "word.h"
#include "slot.h"
#include "square.h"
#include "crossword.h"
#include "utils.h"

using namespace swordsmith;

/**
 * This class implements the standard American Crossword characteristics.
 * The American Crossword class is derived from the public Crossword class.
 */
class AmericanCrossword : public Crossword {

    public:

        /**
         * Standard constructor for inherited American Crossword class.
         */
        AmericanCrossword();

        /**
         * Custom constructor for inherited American Crossword class.
         */
        AmericanCrossword(int rows, int cols);

        /**
         * Standard destructor for inherited American Crossword class.
         */
        ~AmericanCrossword();

        /**
         * Returns American Crossword from 2D array of characters.
         */
        AmericanCrossword FromGrid(std::vector<std::vector<Square>> grid);

        /**
         * Returns whether the slot is an across slot.
         */
        bool IsAcrossSlot(Slot slot);

        /**
         * Returns whether the slot is a down slot.
         */
        bool IsDownSlot(Slot slot);

        /**
         * Returns across and down words as well as their numbers in crossword format.
         */
        std::tuple<std::map<int, Slot>, std::map<int, Slot>> GetClueNumbersAndWords();

        /**
         * Generates the grid from slots without returning anything.
         */
        void GenerateGridFromSlots();

        /**
         * Places block in certain square.
         */
        void PutBlock(int row, int col);

        /**
         * Places list of blocks in specified squares.
         */
        void PutBlocks(std::vector<std::tuple<int, int>> coords);

        /**
         * Adds slot given a set of squares and a word.
         */
        void AddSlot(std::set<Square> squares, Word word);

        /**
         * Generates slots from the stored grid.
         */
        void GenerateSlotsFromGrid();

    private:

        /**
         * Private member variables for the inherited American Crossword class.
         */
        int rows_;
        int cols_;
        std::vector<std::vector<Square*>*>* grid_;

}