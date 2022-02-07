# ⚔️ Swordsmith

Forging crosswords, word by word.

## Developers

- Adam Aaronson
- Jack Joshi
- JT Kirages
- Mark Bauer

## Background

A crossword is a puzzle where the solver must fill a grid of crossing slots with words. Each slot consists of a sequence of squares, where each square is to be filled with a letter. If one square is part of multiple slots, those slots cross at that square. A slot's word is the concatenation of the letters in each of the slot's squares. The grid is validly filled if every slot's word is deemed to be valid.

An American-style crossword consists of a two-dimensional grid of black and white squares, where every maximally contiguous horizontal or vertical sequence of white squares is a slot. In this special case of the crossword, every white square is necessarily part of two slots, a horizontal and vertical slot. Black squares are not part of any slot.

## Problem

Given an unfilled crossword grid and a wordlist of valid words, what is the fastest algorithm to fill the grid with valid words?

### Subproblems

- How can the algorithm be modified to fill the grid in *n* completely different ways?
- How can the algorithm maximize the overall score of the words in the grid, given a scored wordlist?
- How can the algorithm take advantage of linguistic patterns to optimize for American-style crossword grids?