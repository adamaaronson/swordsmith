/**
 * @file tests_slot.cpp
 * Jack Joshi, Adam Aaronson, JT Kirages, Mark Bauer
 * March 2022
 */

#include "../catch/catch.hpp"
#include "../src/slot.h"

TEST_CASE("GetLength") {

    SECTION("Slot that is completely empty") {
        Slot test_slot = Slot();
        REQUIRE(test_slot.GetLength() == 0);
    }

}

