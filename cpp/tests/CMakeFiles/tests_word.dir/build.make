# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.22.2/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.22.2/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/jackjoshi/swordsmith/cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/jackjoshi/swordsmith/cpp

# Include any dependencies generated for this target.
include tests/CMakeFiles/tests_word.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include tests/CMakeFiles/tests_word.dir/compiler_depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/tests_word.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/tests_word.dir/flags.make

tests/CMakeFiles/tests_word.dir/tests_word.cpp.o: tests/CMakeFiles/tests_word.dir/flags.make
tests/CMakeFiles/tests_word.dir/tests_word.cpp.o: tests/tests_word.cpp
tests/CMakeFiles/tests_word.dir/tests_word.cpp.o: tests/CMakeFiles/tests_word.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/jackjoshi/swordsmith/cpp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tests/CMakeFiles/tests_word.dir/tests_word.cpp.o"
	cd /Users/jackjoshi/swordsmith/cpp/tests && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT tests/CMakeFiles/tests_word.dir/tests_word.cpp.o -MF CMakeFiles/tests_word.dir/tests_word.cpp.o.d -o CMakeFiles/tests_word.dir/tests_word.cpp.o -c /Users/jackjoshi/swordsmith/cpp/tests/tests_word.cpp

tests/CMakeFiles/tests_word.dir/tests_word.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tests_word.dir/tests_word.cpp.i"
	cd /Users/jackjoshi/swordsmith/cpp/tests && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/jackjoshi/swordsmith/cpp/tests/tests_word.cpp > CMakeFiles/tests_word.dir/tests_word.cpp.i

tests/CMakeFiles/tests_word.dir/tests_word.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tests_word.dir/tests_word.cpp.s"
	cd /Users/jackjoshi/swordsmith/cpp/tests && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/jackjoshi/swordsmith/cpp/tests/tests_word.cpp -o CMakeFiles/tests_word.dir/tests_word.cpp.s

# Object files for target tests_word
tests_word_OBJECTS = \
"CMakeFiles/tests_word.dir/tests_word.cpp.o"

# External object files for target tests_word
tests_word_EXTERNAL_OBJECTS =

tests/libtests_word.a: tests/CMakeFiles/tests_word.dir/tests_word.cpp.o
tests/libtests_word.a: tests/CMakeFiles/tests_word.dir/build.make
tests/libtests_word.a: tests/CMakeFiles/tests_word.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/jackjoshi/swordsmith/cpp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libtests_word.a"
	cd /Users/jackjoshi/swordsmith/cpp/tests && $(CMAKE_COMMAND) -P CMakeFiles/tests_word.dir/cmake_clean_target.cmake
	cd /Users/jackjoshi/swordsmith/cpp/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tests_word.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/tests_word.dir/build: tests/libtests_word.a
.PHONY : tests/CMakeFiles/tests_word.dir/build

tests/CMakeFiles/tests_word.dir/clean:
	cd /Users/jackjoshi/swordsmith/cpp/tests && $(CMAKE_COMMAND) -P CMakeFiles/tests_word.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/tests_word.dir/clean

tests/CMakeFiles/tests_word.dir/depend:
	cd /Users/jackjoshi/swordsmith/cpp && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/jackjoshi/swordsmith/cpp /Users/jackjoshi/swordsmith/cpp/tests /Users/jackjoshi/swordsmith/cpp /Users/jackjoshi/swordsmith/cpp/tests /Users/jackjoshi/swordsmith/cpp/tests/CMakeFiles/tests_word.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/tests_word.dir/depend

