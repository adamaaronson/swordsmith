# ⚔️ Swordsmith

Forging crosswords, word by word.

## Developers

- Adam Aaronson
- Jack Joshi
- JT Kirages
- Mark Bauer

## Background

A crossword is a puzzle where the solver must fill a grid of crossing slots with words. Each slot consists of a sequence of squares, where each square is to be filled with a letter. If one square is part of multiple slots, the slots are said to be crossing at that square. A slot's word is the concatenation of the letters in each of the slot's squares. The grid is validly filled if every square has a letter and every slot's word is valid.

An American-style crossword consists of a two-dimensional grid of black and white squares, where every maximally contiguous horizontal or vertical sequence of white squares is a slot. In this special case of the crossword, every white square is necessarily part of two slots, a horizontal and vertical slot. Black squares are not part of any slot.

## Problem

Given an unfilled crossword grid and a wordlist of valid words, what is the fastest algorithm to fill the grid with valid words?

### Subproblems

- How can the algorithm be modified to find *n* different word options for a given slot?
- How can the algorithm find a grid with an overall word-score of *n*, given a scored wordlist?
- How can the algorithm take advantage of linguistic patterns to optimize for American-style crossword grids?

## Implementation

- Python
  - Implemented DFS, minlook heuristic, and backjumping for generic and American crosswords
  - Backjumping algorithm can probably be improved, especially for grids constrained by seed entries
  - For implementation details, see the `README` in the [`python` folder](/python).
- C++
  - Work in progress
  - For implementation details, see the [`cpp` folder](/cpp).

## Relevant Papers

- [Computer construction of crossword puzzles using precedence relationships](https://www.sciencedirect.com/science/article/pii/0004370276900199) (Mazlack, 1976)
- [Search Lessons Learned from Crossword Puzzles](https://www.aaai.org/Papers/AAAI/1990/AAAI90-032.pdf) (Ginsberg et al, 1990)
- [Dynamic Backtracking](https://arxiv.org/pdf/cs/9308101.pdf) (Ginsberg, 1993)
- [Constraint Programming Lessons Learned from Crossword Puzzles](https://cs.uwaterloo.ca/~vanbeek/Publications/cai01a.pdf) (Beacham et al, 2001)
- [Crossword Puzzles and Constraint Satisfaction](https://cs.uwaterloo.ca/~vanbeek/Publications/cai01a.pdf) (Connor et al, 2005)

## Contributing

We want Swordsmith to be an open-source sandbox for experimenting with crossword filling algorithms. We encourage you to clone and fork this project to play around with it yourself, and submit pull requests to add your own improvements! Possible contributions might include:

- Improvements to existing filling algorithms
- New filling algorithms that use other strategies
- Implementations in other languages
- Generalizations to other types of puzzles (British-style crosswords, Marching Bands, Rows Garden, etc.)