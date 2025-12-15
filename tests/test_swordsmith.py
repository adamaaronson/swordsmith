import swordsmith as sw
import pytest
import re

GRID_5x = '../swordsmith/grid/5x.txt'
GRID_15x = '../swordsmith/grid/15xcommon.txt'
WORDLIST = '../swordsmith/wordlist/spreadthewordlist.dict'


@pytest.fixture(
    scope='function',
    params=[
        sw.DFSFiller(),
        sw.DFSBackjumpFiller(),
        sw.MinlookFiller(5),
        sw.MinlookBackjumpFiller(5),
    ],
)
def filler(request):
    return request.param


@pytest.fixture(
    scope='function',
    params=[
        GRID_5x,
        GRID_15x,
    ],
)
def grid_path(request):
    return request.param


def test_fill(filler, grid_path):
    grid = sw.read_grid(grid_path)
    crossword = sw.AmericanCrossword.from_grid(grid)
    wordlist = sw.read_wordlist(WORDLIST)

    filler.fill(crossword, wordlist, animate=False)

    assert crossword.is_validly_filled(wordlist)


@pytest.mark.parametrize(
    'constrained_slot',
    [
        ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)),
        ((4, 0), (4, 1), (4, 2), (4, 3), (4, 4)),
    ],
)
@pytest.mark.parametrize('regex', [r'^[^AEIOUY]*$', r'^[AEIOUY]*$'])
def test_regex_constraints(constrained_slot, regex, filler):
    grid = sw.read_grid(GRID_5x)
    crossword = sw.AmericanCrossword.from_grid(grid)
    crossword.add_regex_constraint(constrained_slot, regex)
    wordlist = sw.read_wordlist(WORDLIST)

    filler.fill(crossword, wordlist, animate=False)

    assert crossword.is_validly_filled(wordlist)
    assert re.search(regex, crossword.words[constrained_slot]) is not None


@pytest.mark.parametrize(
    'constrained_slot',
    [
        ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)),
        ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
    ],
)
@pytest.mark.parametrize('upscored_word', ['BANJO', 'ZEBRA'])
def test_score_constraints(constrained_slot, upscored_word, filler):
    grid = sw.read_grid(GRID_5x)
    crossword = sw.AmericanCrossword.from_grid(grid)
    crossword.add_score_constraint(constrained_slot, 80)
    wordlist = sw.read_wordlist(WORDLIST)
    wordlist.scores[upscored_word] = 80

    filler.fill(crossword, wordlist, animate=False)

    assert crossword.is_validly_filled(wordlist)
    assert crossword.words[constrained_slot] == upscored_word
