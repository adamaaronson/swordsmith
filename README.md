# ⚔️ Swordsmith

Forging crosswords, word by word.

### Developers

- Adam Aaronson
- Jack Joshi
- JT Kirages
- Mark Bauer

---

## How to Use

From the `tests` folder, run the command:

```
python3 test_swordsmith.py
```

Using any of these optional command line flags:

| Flag | Short | Description |
|------------|----|-----------------------|
| --wordlist WORDLIST_PATH | -w | filepath for wordlist |
| --database DATABASE_PATH | -d | filepath for database |
| --grid GRID_PATH | -g | filepath for grid     |
| --num_trials NUM_TRIALS | -t | number of grids to try filling |
| --k K | -k | k constant for minlook |
| --strategy [dfs minlook] | -s | which filling algorithm to run |
| --animate | -a | whether to animate grid filling |

For example:

```
python3 test_swordsmith.py -w wordlist/spreadthewordlist.dict -g grids/7xopen.txt -a
```

---

## Wordlist

Contains the collection of words to be used while filling a crossword, as well as the pattern-matching functionality for filling an incomplete slot.

### Fields
- `words`
	- Set of words in the wordlist
- `added_words`
	- Set of words that weren't originally in the wordlist, but were added while the program was running
- `pattern_matches`
	- Dictionary that holds previously searched patterns matched with the database
- `conn` and `cur`
	- Connection and cursor to interface with the sqlite database of words

### Methods
- `add_word(self, word)`
	- Adds `word` to the wordlist
- `remove_word(self, word)`
	- Removes `word` from the wordlist
- `init_database(self)`
	- Initializes sqlite database of words
	- One table for each word length
		- One row for each word
		- `i`th column represents the letter at the `i`th index of the word
- `get_matches(self, pattern)`
	- Returns list of words in the wordlist that match `pattern`
	- `pattern` is a string with any number of wildcard (`EMPTY`) characters
---

## Slot

Represents a position in a grid where a word can go.

Simply a namedtuple of `row`, `col`, and `dir`, where `dir` is either `ACROSS` or `DOWN`.

TODO: Slots should probably contain their length and/or a list of squares they correspond to, maybe instead of the direction

TODO: Should probably have a namedtuple for `Square` as well

---
## Crossword

Represents a rectangular grid of squares (`(row, col)` pairs). Squares comprise slots, which contain entries. Entries are strings whose `i`th character corresponds to the `i`th square of the slot. Entries can be filled, partially `EMPTY`, or completely `EMPTY`.

If two slots contain the same square, their entries "cross" at that square and their letters corresponding to that square must be the same.

TODO: Clear up "entry" and "word" terminology, I think it works to say a word is a completely filled entry

### Fields
- `rows`
	- Number of rows in the grid
- `cols`
	- Number of columns in the grid
- `grid`
	- `rows` by `cols` array of characters representing the letters in each square of the grid
- `wordlist`
	- Wordlist that contains all of the crossword's filled entries
	- TODO: This probably shouldn't be held in the Crossword class, seems anti-encapsulation
- `entries`
	- Dictionary mapping each `Slot` to its corresponding entry
	- Should be updated as grid is filled
- `entryset`
	- Set of filled entries in the grid
	- Used for dupe detection
	- Should be updated as grid is filled
- `across_slots`
	- Dictionary mapping each non-`BLOCK` square to the `ACROSS` `Slot` containing it
- `down_slots`
	- Dictionary mapping each non-`BLOCK` square to the `DOWN` `Slot` containing it
	- TODO: These should really be held in one dictionary somehow, the current implementation is super repetitive and inelegant
- `squares_in_slot`
	- Dictionary mapping each `Slot` to a list of squares it contains
	- TODO: This should probably be a property of `Slot`, not `Crossword`
- `slots_crossing_slot`
	- Dictionary mapping each `Slot` to a set of `Slot`s it crosses

### Class Methods
- `from_grid(cls, grid, wordlist=None)`
	- Constructs a crossword from the given `grid` 2D array and `wordlist`

### Methods
- `is_letter(self, row, col)`
	- Returns whether the given square contains a letter, i.e. is not `EMPTY` or `BLOCK`
- `put_block(self, row, col)`
	- Places `BLOCK` at given square
- `put_blocks(self, coords)`
	- Places `BLOCK` at all of the given squares in the list `coords`
- `put_letter(self, slot, i, letter)`
	- Places given `letter` at `i`th square of given `slot`
	- Does not update crossing slots
- `put_word(self, word, slot, add_to_wordlist=True)`
	- Places `word` in the given `slot`
	- By default it should add it to the wordlist if it isn't already included, but if a filler is restoring a previous word then `add_to_wordlist` can be set to `False`
	- Updates entries in crossing slots using `put_letter`
- `generate_slots(self)`
	- Processes `grid` array to create all the `Slot` dictionary fields
	- Called whenever grid shape changes
	- TODO: This function is a behemoth, make it better
- `print_words(self)`
	- Neatly prints out all the entries in the grid
- `fewest_matches(self)`
	- Returns the unfilled `Slot` in the grid with the fewest matches according to the `wordlist`, as well as its number of matches
	- Used as a next-slot heuristic
- `is_filled(self, word)`
	- Returns whether `word` is completely filled
	- TODO: This has no business being in the `Crossword` class
- `is_grid_filled(self)`
	- Returns whether every square in the grid is non-`EMPTY`
- `has_valid_words(self)`
	- Returns whether every filled entry is in the `wordlist`
- `is_dupe(self, word)`
	- Returns whether `word` is a dupe, i.e. whether it's already in the `entryset`
- `get_crossing_entries(self, slot, word=None)`
	- Returns entries that would cross the given `slot` if the given `word` was entered into it, without actually placing the `word` in
	- Used for `minlook` heuristic
- `minlook(self, slot, k, matches)`
	- Randomly looks at `k` possible `matches`
	- Returns index of match that yields the most possible crossing entries if it were placed in the `slot`, as well as the indices of matches that immediately cause inconsistencies
	- Determines number of crossing entries by computing the sum of logarithms of crossing match counts
	- Used for `minlook` and `arc-consistency` heuristic

---

## Filler

Abstract Base Class for an algorithm that fills a `Crossword`.

### Abstract Methods
- `fill(self, crossword, animate)`
	- Fills the given `crossword` using some strategy
	- Can optionally `animate` the filling process by printing out the grid at each step

---

## DFSFiller

Implementation of `Filler` that uses a naive DFS algorithm.

### Methods
- `fill(self, crossword, animate)`
	- If the grid is already filled, just return `True`
	- Choose next `Slot` to fill using `fewest_matches` heuristic
		- If `num_matches` is zero, crossword is unfillable, return `False`
	- Randomly iterate through all possible matches for that `Slot`
		- If the match can be placed without creating a dupe or invalid word, then recurse
	- If none of the matches worked, restore the `Slot`'s previous entry and return `False`

---

## MinlookFiller

Implementation of `Filler` that uses a naive DFS algorithm.

### Fields
- `k`
	- Number of potential matches to look ahead to at each fill step

### Methods
- `fill(self, crossword, animate)`
	- If the grid is already filled, just return `True`
	- Choose next `Slot` to fill using `fewest_matches` heuristic
		- If `num_matches` is zero, crossword is unfillable, return `False`
	- Use `minlook` to look ahead to at most `k` random matches and find the one that yields the most possible crossing matches
		- Throw out both the chosen match and the failed matches from the matches list
		- If the chosen match can be placed without creating a dupe or invalid word, then recurse
		- If the chosen match didn't work and there are more matches to try, use `minlook` again
	- If none of the matches worked, restore the `Slot`'s previous entry and return `False`
