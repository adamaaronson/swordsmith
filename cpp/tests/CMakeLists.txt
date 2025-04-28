# TEST SWORDSMITH
add_library(tests_word tests_word.cpp)
add_library(tests_square tests_square.cpp)
add_library(tests_slot tests_slot.cpp)
add_library(tests_wordlist tests_wordlist.cpp)
add_library(tests_crossword tests_crossword.cpp)
target_link_libraries(test LINK_PUBLIC square word slot wordlist crossword)