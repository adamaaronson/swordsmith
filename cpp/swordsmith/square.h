/**
 * @file square.h
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#pragma once

#include <tuple>

using namespace swordsmith;

/**
 * This class represents a Square within the Crossword framework.
 */
class Square {

    public:

        /**
         * Standard constructor for Square class.
         */
        Square();

        /**
         * Custom constructor for Square class.
         */
        Square(std::tuple<int, int> coordinates, char letter);

        /**
         * Standard destructor for Square class.
         */
        ~Square();

    private:

        /**
         * Private member variables storing the letter and coordinates of the Square.
         */
        std::tuple<int, int> coordinates_;
        char letter_;

};