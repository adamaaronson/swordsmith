/**
 * @file american_crossword.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "american_crossword.h"

/**
 * Standard constructor for inherited American Crossword class.
 */
AmericanCrossword::AmericanCrossword() {}

/**
 * Custom constructor for inherited American Crossword class.
 */
AmericanCrossword::AmericanCrossword(int rows, int cols) {

    rows_ = rows;
    cols_ = cols;

    grid_->reserve(rows);
    for (int r : r < rows; r++) {
        grid_[r]->reserve(cols);
    }

    for (int r : r < rows; r++) {
        for (int c : c < cols; c++) {
            Square * square = new Square();
            grid_[r][c] = square;
        }
    }

    GenerateSlotsFromGrid();

}

/**
 * Standard destructor for inherited American Crossword class.
 */
~AmericanCrossword::AmericanCrossword() {

    for (int r : r < rows; r++) {
        for (int c : c < cols; c++) {
            delete grid_[r][c]
        }
        delete[] grid_[r]
    }
    delete[] grid_

}

/**
 * Returns American Crossword from 2D array of characters.
 */
AmericanCrossword AmericanCrossword::FromGrid(std::vector<std::vector<Square>> grid) {

    #warning "do we want to pass in a pointer to grid or something?"
    rows = grid.size();
    cols = grid[0].size();

    std::vector<std::tuple<int, int>> blocks;

    for (int r : r < rows; r++) {
        for (int c : c < cols; c++) {
            if (grid[r][c].GetLetter() == BLOCK) {
                std::tuple<int, int> block = std::make_tuple(r, c);
                blocks.append(block);
            }
        }
    }

    #warning "Does this make sense in C++"
    AmericanCrossword * xw = AmericanCrossword(rows, cols);
    if (blocks.size() > 0) {
        xw->putBlocks(blocks);
    }

    for (int r : r < rows; r++) {
        for (int c : c < cols; c++) {
            if ((grid[r][c]->GetLetter() != BLOCK) && (grid[r][c]->GetLetter() != EMPTY)) {
                xw->grid_[r][c] = grid[r][c];
            }
        }
    }

    xw->GenerateSlotsFromGrid();

    return xw;

}

/**
 * Returns whether the slot is an across slot.
 */
bool AmericanCrossword::IsAcrossSlot(Slot slot) {
    return slot.IsAcross();
}

/**
 * Returns whether the slot is a down slot.
 */
bool AmericanCrossword::IsDownSlot(Slot slot) {
    return slot.IsDown();
}

/**
 * Returns across and down words as well as their numbers in crossword format.
 */
std::tuple<std::map<int, Slot>, std::map<int, Slot>> AmericanCrossword::GetClueNumbersAndWords() {
    
    int square_index = 1;

    std::set<Slot> across_slots;
    std::set<Slot> down_slots;

    std::map<int, Slot> across_words;
    std::map<int, Slot> down_words;

    for (int r : r < rows_; r++) {
        for (int c : c < cols_; c++) {

            bool increment_index = false;
            Square * square = grid_[r][c];

            for (Slot slot : squares_[square]) {
                #warning "Does squares_ get inherited from crossword class?"
                
                if ((IsAcrossSlot(slot)) && (!across_slots.contains(slot)) {
                    across_slots.insert(slot);
                    across_words[square_index] = words_[slot];
                    increment_index = true;
                }
                
                if ((IsDownSlot(slot)) && (!down_slots.contains(slot))) {
                    down_slots.insert(slot);
                    down_words[square_index] = words_[slot];
                    increment_index = true;
                }

            }

            if (increment_index) {
                square_index++;
            }
        }
    }

    std::tuple<std::map<int, Slot>, std::map<int, Slot>> output;
    output = make_tuple(across_words, down_words);

    return output;

}

/**
 * Generates the grid from slots without returning anything.
 */
void AmericanCrossword::GenerateGridFromSlots() {

    std::set<Slot>::iterator it = slots_.begin();
    while (it != slots_.end()) {
        Slot slot = *it;
        for (int i : i < slot.GetLength(); i++) {
            Square square = slot.GetSquares()[i];
            std::tuple<int, int> coords = square.GetCoordinates();
            int row = std::get<0>(coords);
            int col = std::get<1>(coords);
            grid_[row][col] = square;
        }
    }

}

#warning "Include __str__ function from python implementation somehow"

/**
 * Places block in certain square.
 */
void AmericanCrossword::PutBlock(int row, int col) {

    std::tuple<int, int> coords = std::make_tuple(row, col);
    Square * square = new Square(coords, BLOCK);
    grid_[row][col] = square;

    GenerateSlotsFromGrid();

}

/**
 * Places list of blocks in specified squares.
 */
void AmericanCrossword::PutBlocks(std::vector<std::tuple<int, int>> coords) {

    for (int i : i < coords.size(); i++) {
        int row = std::get<0>(coords[i]);
        int col = std::get<1>(coords[i]);
        Square * square = new Square(coords[i], BLOCK);
        grid_[row][col] = square;
    }

    GenerateSlotsFromGrid();

}

/**
 * Adds slot given a set of squares and a word.
 */
void AmericanCrossword::AddSlot(std::set<Square> squares, Word word) {

    #warning "Implement this function"

}

/**
 * Generates slots from the stored grid.
 */
void AmericanCrossword::GenerateSlotsFromGrid() {

    #warning "Implement this function"
    
}