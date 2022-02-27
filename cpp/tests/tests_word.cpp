/**
 * @file tests_word.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * February 2022
 */

#include <iostream>

#define CATCH_CONFIG_MAIN
#include "../catch/catch.hpp"
#include "../src/word.h"

TEST_CASE("IsFilled") {

    SECTION("Word that is completely empty") {
        Word test_word = Word();
        REQUIRE(~test_word.IsFilled());
    }

    SECTION("Word with lowercase letters") {
        Word test_word = Word("abcdefg");
        REQUIRE(test_word.IsFilled());
    }

    SECTION("Word with uppercase letters") {
        Word test_word = Word("ABCDCBA");
        REQUIRE(test_word.IsFilled());
    }

    SECTION("Word with letters and numbers") {
        Word test_word = Word("test123test456");
        REQUIRE(test_word.IsFilled());
    }

    SECTION("Word with letters and punctuation") {
        Word test_word = Word("test{:?#$!./");
        REQUIRE(test_word.IsFilled());
    }

    SECTION("Word with letters and empty characters") {
        Word test_word = Word("test test");
        REQUIRE(~test_word.IsFilled());
    }

}

TEST_CASE("GetWord") {

    SECTION("Word that is completely empty") {
        Word test_word = Word();
        std::string output = test_word.GetWord();
        REQUIRE(output == "");
    }

    SECTION("Word that has all characters") {
        Word test_word = Word("Ah43f2]c;]f;3]_ 3oni:test");
        std::string output = test_word.GetWord();
        REQUIRE(output == "Ah43f2]c;]f;3]_ 3oni:test");
    }

}