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
include src/CMakeFiles/word.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include src/CMakeFiles/word.dir/compiler_depend.make

# Include the progress variables for this target.
include src/CMakeFiles/word.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/word.dir/flags.make

src/CMakeFiles/word.dir/word.cpp.o: src/CMakeFiles/word.dir/flags.make
src/CMakeFiles/word.dir/word.cpp.o: src/word.cpp
src/CMakeFiles/word.dir/word.cpp.o: src/CMakeFiles/word.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/jackjoshi/swordsmith/cpp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/word.dir/word.cpp.o"
	cd /Users/jackjoshi/swordsmith/cpp/src && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT src/CMakeFiles/word.dir/word.cpp.o -MF CMakeFiles/word.dir/word.cpp.o.d -o CMakeFiles/word.dir/word.cpp.o -c /Users/jackjoshi/swordsmith/cpp/src/word.cpp

src/CMakeFiles/word.dir/word.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/word.dir/word.cpp.i"
	cd /Users/jackjoshi/swordsmith/cpp/src && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/jackjoshi/swordsmith/cpp/src/word.cpp > CMakeFiles/word.dir/word.cpp.i

src/CMakeFiles/word.dir/word.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/word.dir/word.cpp.s"
	cd /Users/jackjoshi/swordsmith/cpp/src && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/jackjoshi/swordsmith/cpp/src/word.cpp -o CMakeFiles/word.dir/word.cpp.s

# Object files for target word
word_OBJECTS = \
"CMakeFiles/word.dir/word.cpp.o"

# External object files for target word
word_EXTERNAL_OBJECTS =

src/libword.a: src/CMakeFiles/word.dir/word.cpp.o
src/libword.a: src/CMakeFiles/word.dir/build.make
src/libword.a: src/CMakeFiles/word.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/jackjoshi/swordsmith/cpp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libword.a"
	cd /Users/jackjoshi/swordsmith/cpp/src && $(CMAKE_COMMAND) -P CMakeFiles/word.dir/cmake_clean_target.cmake
	cd /Users/jackjoshi/swordsmith/cpp/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/word.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/word.dir/build: src/libword.a
.PHONY : src/CMakeFiles/word.dir/build

src/CMakeFiles/word.dir/clean:
	cd /Users/jackjoshi/swordsmith/cpp/src && $(CMAKE_COMMAND) -P CMakeFiles/word.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/word.dir/clean

src/CMakeFiles/word.dir/depend:
	cd /Users/jackjoshi/swordsmith/cpp && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/jackjoshi/swordsmith/cpp /Users/jackjoshi/swordsmith/cpp/src /Users/jackjoshi/swordsmith/cpp /Users/jackjoshi/swordsmith/cpp/src /Users/jackjoshi/swordsmith/cpp/src/CMakeFiles/word.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/word.dir/depend

