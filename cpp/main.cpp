/**
 * @file main.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "src/word.h"

#include <iostream>

int main() {

    Word test_word = Word("ItWorks!");
    if (test_word.IsFilled()) {
        std::cout << test_word.getWord() << std::endl;
    }

    return 0;

}