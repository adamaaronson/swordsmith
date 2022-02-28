cmake_minimum_required(VERSION 3.22.2)

# RUN SWORDSMITH
project(swordsmith)
add_executable(${PROJECT_NAME} main.cpp)
add_subdirectory(src)
target_link_libraries(${PROJECT_NAME} word)

# TEST SWORDSMITH
project(test)
add_executable(${PROJECT_NAME} tests/tests_word.cpp tests/tests_square.cpp)
add_subdirectory(tests)
target_link_libraries(${PROJECT_NAME} tests_word word tests_square square)