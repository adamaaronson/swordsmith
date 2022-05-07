/**
 * @file square.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "square.h"

/**
 * Standard constructor for Square class.
 */
Square::Square() {
    #warning "How do we want to store EMPTY and BLOCK? Globally or locally?"
    EMPTY = '.';
    letter_ = EMPTY;
    coordinates_ = std::make_tuple(0, 0);
}

/**
 * Custom constructor for Square class.
 */
Square::Square(std::tuple<int, int> coordinates, char letter) {
    EMPTY = '.';
    coordinates_ = coordinates;
    letter_ = letter;
}

/**
 * Standard destructor for Square class.
 */
Square::~Square() {}

/**
 * Returns the coordinates of the Square.
 */
std::tuple<int, int> Square::GetCoordinates() {
    return coordinates_;
}

/**
 * Returns the letter that the Square contains.
 */
char Square::GetLetter() {
    return letter_;
}