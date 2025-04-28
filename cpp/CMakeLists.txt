# SET VERSION REQUIREMENTS
cmake_minimum_required(VERSION 3.22.2)
set(CMAKE_CXX_STANDARD 20)

# RUN SWORDSMITH
project(swordsmith)
add_executable(${PROJECT_NAME} main.cpp)
add_subdirectory(src)
target_link_libraries(${PROJECT_NAME} word square slot wordlist crossword)

# TEST SWORDSMITH
project(test)
add_executable(${PROJECT_NAME} tests/tests_word.cpp tests/tests_square.cpp 
                               tests/tests_slot.cpp tests/tests_wordlist.cpp
                               tests/tests_crossword.cpp)
add_subdirectory(tests)
target_link_libraries(test LINK_PUBLIC tests_word tests_square tests_slot
                                       tests_wordlist tests_crossword)