/**
 * @file slot.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <tuple>

using namespace swordsmith;

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
         * Standard destructor for the Slot class.
         */
        ~Slot();

        /**
         * Returns the length of the slot.
         */
        int GetLength();

    private:

        /**
         * Private member variables for the slot class.
         */
        int length_;
        std::vector<Square> squares_;

}