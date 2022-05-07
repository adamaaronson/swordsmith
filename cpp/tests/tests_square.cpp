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
        REQUIRE(isblank(test_square.GetLetter()));
    }

    SECTION("Square that is filled with a letter") {
        std::tuple<int, int> test_coords = std::make_tuple(3, 4);
        Square test_square = Square(test_coords, 'a');
        REQUIRE(test_square.GetLetter() == 'a');
    }

    SECTION("Square that is filled with a number") {
        std::tuple<int, int> test_coords = std::make_tuple(3, 4);
        Square test_square = Square(test_coords, '3');
        REQUIRE(test_square.GetLetter() == '3');
    }

}

TEST_CASE("GetCoordinates") {

    SECTION("Square that has no specified coordinates") {
        Square test_square = Square();
        std::tuple<int, int> test_coords = test_square.GetCoordinates();
        REQUIRE(std::get<0>(test_coords) == 0);
        REQUIRE(std::get<1>(test_coords) == 0);
    }

    SECTION("Square that has specified coordinates") {
        std::tuple<int, int> input_coords = std::make_tuple(3, 4);
        Square test_square = Square(input_coords, 'a');
        std::tuple<int, int> test_coords = test_square.GetCoordinates();
        REQUIRE(std::get<0>(test_coords) == 3);
        REQUIRE(std::get<1>(test_coords) == 4);
    }

}