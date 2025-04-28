/**
 * @file slot.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "slot.h"

/**
 * Standard constructor for the Slot class.
 */
Slot::Slot() {
    length_ = 0;
}

/**
 * Custom constructor for the Slot class.
 */
Slot::Slot(int length, bool across, bool down) {
    length_ = length;
    across_ = across;
    down_ = down;
    squares_.reserve(length);
}

/**
 * Second custom constructor for the Slot class.
 */
Slot::Slot(int length, std::vector<Square> squares) {
    length_ = length;
    squares_.reserve(length);
    squares_ = squares;
}

/**
 * Standard destructor for the Slot class.
 */
Slot::~Slot() {}

/**
 * Returns the length of the slot.
 */
int Slot::GetLength() {
    return length_;
}

/**
 * Returns the stored vector of squares.
 */
std::vector<Square> Slot::GetSquares() {
    return squares_;
}

/**
 * Add square to index of slot.
 */
void Slot::AddSquare(int index, Square square) {
    squares_[index] = square;
}

/**
 * Return whether the slot is an across slot.
 */
bool IsAcross() {
    return across_;
}

/**
 * Return whether the slot is down slot.
 */
bool IsDown() {
    return down_;
}