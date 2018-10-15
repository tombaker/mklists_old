import pytest
import os
from mklists.rule import Rule, _line_matches
from mklists import VALID_FILENAME_CHARS

@pytest.mark.line_matches
def test_line_matches():
    _line_matches(matchpattern='NOW', matchfield=1, dataline='NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_with_space():
    _line_matches(matchpattern='NOW', matchfield=1, dataline=' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_no_match():
    _line_matches(matchpattern='NOW', matchfield=1, dataline='LATER Buy milk') == False

@pytest.mark.line_matches
def test_line_matches_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    _line_matches(matchpattern='^NOW', matchfield=1, dataline=' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_entire_line():
    _line_matches(matchpattern="^NOW", matchfield=0, dataline='NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_positional():
    _line_matches('NOW', 1, 'NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_positional_with_space():
    _line_matches('NOW', 1, ' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_positional_no_match():
    _line_matches('NOW', 1, 'LATER Buy milk') == False

@pytest.mark.line_matches
def test_line_matches_positional_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    _line_matches('^NOW', 1, ' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_positional_entire_line():
    _line_matches("^NOW", 0, 'NOW Buy milk') == True


def test_has_been_initialized():
    x = Rule(1, 'NOW', 'a.txt', 'b.txt', 0)
    x._source_has_been_initialized()
    y = Rule(1, 'LATER', 'b.txt', 'c.txt', 0)
    assert y._source_has_been_initialized()

@pytest.mark.skip
def test_source_is_registered_not():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    Rule.register(x)
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    with pytest.raises(SystemExit):
        Rule.register(y)

def test_is_valid_not():
    x = Rule(1, 'N(OW', 'a', 'b', 2)
    with pytest.raises(SystemExit):
        x.is_valid(VALID_FILENAME_CHARS)

def test_rule():
    x = Rule(1, '.', 'a', 'b', 2)
    assert x.source == 'a'

def test_rulestring_regex_has_space():
    x = Rule(1, '^X 19', 'a', 'b', 2)
    assert x.source_matchpattern == '^X 19'

def test_source_filename_valid():
    x = Rule(1, '^X 19', 'a.txt', 'b.txt', 2)
    assert x._source_and_target_filenames_are_valid(VALID_FILENAME_CHARS)

def test_target_filename_valid():
    x = Rule(1, '^X 19', 'a.txt', 'b.txt', 2)
    assert x._source_and_target_filenames_are_valid(VALID_FILENAME_CHARS)

def test_target_filename_valid_not():
    x = Rule(1, '^X 19', 'a.txt', 'b^.txt', 2)
    with pytest.raises(SystemExit):
        x._source_and_target_filenames_are_valid(VALID_FILENAME_CHARS)

def test_source_matchfield_and_target_sortorder_are_valid():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_and_target_sortorder_are_integers

def test_source_matchfield_and_target_sortorder_are_integers():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_and_target_sortorder_are_integers

def test_source_ne_target():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_is_not_equal_target

def test_source_ne_target_not():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_is_not_equal_target()

def test_source_matchpattern_is_valid():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    assert x._source_matchpattern_is_valid

def test_source_matchpattern_is_valid_not():
    x = Rule('1', 'N(OW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()
