import pytest
import os
from mklists.rule import Rule, apply_rules_to_datalines, _line_matches
from mklists import VALID_FILENAME_CHARS

@pytest.mark.apply_rules
def test_apply_rules():
    rules = [Rule(1, 'NOW', 'a.txt', 'now.txt', 0),
             Rule(1, 'LATER', 'a.txt', 'later.txt', 0)]
    lines = ['NOW Summer\n', 'LATER Winter\n']
    mdict = {'now.txt': ['NOW Summer\n'], 
             'later.txt': ['LATER Winter\n'],
             'a.txt': []}
    apply_rules_to_datalines(rules, lines) == mdict

@pytest.mark.apply_rules
def test_apply_rules_no_data():
    rules = [Rule(1, 'NOW', 'a.txt', 'now.txt', 0),
             Rule(1, 'LATER', 'a.txt', 'later.txt', 0)]
    lines = []
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)

@pytest.mark.apply_rules
def test_apply_rules_no_rules():
    rules = []
    lines = ['NOW Summer\n', 'LATER Winter\n']
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)

@pytest.mark.apply_rules
def test_apply_rules_sorted():
    rules = [Rule(1, '.', 'a.txt', 'now.txt', 1)]
    lines = ['LATER Winter\n', 'NOW Summer\n']
    mdict = {'now.txt': ['NOW Summer\n', 'LATER Winter\n'], 
             'a.txt': []}
    apply_rules_to_datalines(rules, lines) == mdict

@pytest.mark.line_matches
def test_line_matches():
    given_rule = Rule(1, 'NOW', 'a.txt', 'b.txt', 0)
    _line_matches(given_rule, 'NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_with_space():
    given_rule = Rule(1, 'NOW', 'a.txt', 'b.txt', 0)
    _line_matches(given_rule, ' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_no_match():
    given_rule = Rule(1, 'NOW', 'a.txt', 'b.txt', 0)
    _line_matches(given_rule, 'LATER Buy milk') == False

@pytest.mark.line_matches
def test_line_matches_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    given_rule = Rule(1, '^NOW', 'a.txt', 'b.txt', 0)
    _line_matches(given_rule, ' NOW Buy milk') == True

@pytest.mark.line_matches
def test_line_matches_entire_line():
    given_rule = Rule(0, '^NOW', 'a.txt', 'b.txt', 0)
    _line_matches(given_rule, 'NOW Buy milk') == True

@pytest.mark.rule
def test_has_been_initialized():
    x = Rule(1, 'NOW', 'a.txt', 'b.txt', 0)
    x._source_has_been_initialized()
    y = Rule(1, 'LATER', 'b.txt', 'c.txt', 0)
    assert y._source_has_been_initialized()

@pytest.mark.rule
def test_source_is_registered_not():
    """Rule class keeps track of instances registered, so 
    second rule instance 'y' should raise exception because 
    'c.txt' will not have been registered as a source."""
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    y._source_has_been_initialized() == False

@pytest.mark.rule
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
