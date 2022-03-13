/**
 * @file tests_square.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include "../catch/catch.hpp"
#include "../src/square.h"

TEST_CASE("GetLetter") {

    SECTION("Square that is completely empty") {
        Square test_square = Square();
        REQUIRE(~isblank(test_square.GetLetter()));
        REQUIRE(1 == 1);
    }

    SECTION("Square that is filled with a letter") {
        std::tuple<int, int> test_coords = std::make_tuple(3, 4);
        Square test_square = Square(test_coords, 'a');
        REQUIRE(test_square.GetLetter() == 'a');
    }

}