/**
 * @file american_crossword.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "american_crossword.h"

/**
 * Standard constructor for inherited American Crossword class.
 */
AmericanCrossword::AmericanCrossword();

/**
 * Custom constructor for inherited American Crossword class.
 */
AmericanCrossword::AmericanCrossword(int rows, int cols);

/**
 * Standard destructor for inherited American Crossword class.
 */
~AmericanCrossword::AmericanCrossword();

/**
 * Returns American Crossword from 2D array of characters.
 */
Crossword AmericanCrossword::FromGrid(std::vector<std::vector<Square>> grid);

/**
 * Returns whether the slot is an across slot.
 */
bool AmericanCrossword::IsAcrossSlot(Slot slot);

/**
 * Returns whether the slot is a down slot.
 */
bool AmericanCrossword::IsDownSlot(Slot slot);

/**
 * Returns across and down words as well as their numbers in crossword format.
 */
std::tuple<std::map<int, Slot>, std::map<int, Slot>> AmericanCrossword::GetClueNumbersAndWords();

/**
 * Generates the grid from slots without returning anything.
 */
void AmericanCrossword::GenerateGridFromSlots();

/**
 * Places block in certain square.
 */
void AmericanCrossword::PutBlock(int row, int col);

/**
 * Places list of blocks in specified squares.
 */
void AmericanCrossword::PutBlocks(std::vector<std::tuple<int, int>> coords);

/**
 * Adds slot given a set of squares and a word.
 */
void AmericanCrossword::AddSlot(std::set<Square> squares, Word word);

/**
 * Generates slots from the stored grid.
 */
void AmericanCrossword::GenerateSlotsFromGrid();