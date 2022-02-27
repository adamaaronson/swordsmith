cmake_minimum_required(VERSION 3.22.2)

project(swordsmith)

add_executable(${PROJECT_NAME} main.cpp)

add_subdirectory(src)

target_link_libraries(${PROJECT_NAME} word)