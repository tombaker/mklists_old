import pytest
from mklists.rule import *


def test_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    assert x.source == 'a'

def test_rulestring_regex_has_space():
    x = Rule('1', '^X 19', 'a', 'b', '2')
    assert x.source_matchpattern == '^X 19'

def test_source_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x.source_filename_valid()

def test_target_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x.target_filename_valid()

def test_target_filename_valid_not():
    x = Rule('1', '^X 19', 'a.txt', 'b^.txt', '2')
    with pytest.raises(SystemExit):
        x.target_filename_valid()

def test_register_source_ok():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    x.register_source()
    y = Rule('1', 'LATER', 'b.txt', 'c.txt', '0')
    assert y.register_source

def test_register_source_not():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    x.register_source()
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    with pytest.raises(SystemExit):
        y.register_source()

# source_matchfield, source_matchpattern, source, target, target_sortorder

def test_source_matchfield_is_digit():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x.source_matchfield_is_digit

def test_target_sortorder_is_digit():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x.target_sortorder_is_digit

def test_source_ne_target():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x.source_not_equal_target

def test_source_ne_target_not():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x.source_not_equal_target()

#def test_rulestring_is_empty():
#def test_rulestring_is_comment_only():
#def test_srules_to_lrules():
#def test_check_lrule_field1_error_exit():
