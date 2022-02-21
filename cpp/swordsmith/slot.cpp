/**
 * @file slot.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "slot.h"

/**
 * Standard constructor for the Slot class.
 */
Slot::Slot() {}

/**
 * Custom constructor for the Slot class.
 */
Slot::Slot(int length) {
    length_ = length;
    squares_.reserve(length);
}

/**
 * Standard destructor for the Slot class.
 */
~Slot::Slot() {}

/**
 * Returns the length of the slot.
 */
int Slot::GetLength() {
    return length_;
}