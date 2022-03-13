# TEST SWORDSMITH
project(test)
add_library(tests_word tests_word.cpp)
add_library(tests_square tests_square.cpp)
add_executable(${PROJECT_NAME} tests_word tests_square)
target_link_libraries(test LINK_PUBLIC square word)