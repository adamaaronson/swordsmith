/**
 * @file square.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "square.h"

/**
 * Standard constructor for Square class.
 */
Square::Square() {}

/**
 * Custom constructor for Square class.
 */
Square::Square(std::tuple<int, int> coordinates, char letter) {
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