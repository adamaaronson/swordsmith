/**
 * @file slot.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <vector>

#include "square.h"

/**
 * This class implements the Slot framework.
 */
class Slot {

    public:

        /**
         * Standard constructor for the Slot class.
         */
        Slot();

        /**
         * Custom constructor for the Slot class.
         */
        Slot(int length);

        /**
         * Second custom constructor for the Slot class.
         */
        Slot(int length, std::vector<Square> squares);

        /**
         * Standard destructor for the Slot class.
         */
        ~Slot();

        /**
         * Returns the length of the slot.
         */
        int GetLength();

        /**
         * Returns the stored vector of squares.
         */
        std::vector<Square> GetSquares();

        /**
         * Add square to index of slot.
         */
        void AddSquare(int index, Square square);

        /**
         * Return whether the slot is an across slot.
         */
        bool IsAcross();

        /**
         * Return whether the slot is down slot.
         */
        bool IsDown();

    private:

        /**
         * Private member variables for the slot class.
         */
        int length_;
        std::vector<Square> squares_;
        bool across_;
        bool down_;

};