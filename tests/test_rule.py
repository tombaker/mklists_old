import pytest
from mklists.rules import *

@pytest.mark.rule
def test_validate_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    y = Rule(1, '.', 'a', 'b', 2)
    assert x.validate() == y

@pytest.mark.rule
def test_validate_rule_not():
    x = Rule('1', 'N(OW', 'a', 'b', '2')
    with pytest.raises(SystemExit):
        x.validate()

@pytest.mark.rule
def test_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    assert x.source == 'a'

@pytest.mark.rule
def test_rulestring_regex_has_space():
    x = Rule('1', '^X 19', 'a', 'b', '2')
    assert x.source_matchpattern == '^X 19'

@pytest.mark.rule
def test_source_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._source_filename_valid()

@pytest.mark.rule
def test_target_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._target_filename_valid()

@pytest.mark.rule
def test_target_filename_valid_not():
    x = Rule('1', '^X 19', 'a.txt', 'b^.txt', '2')
    with pytest.raises(SystemExit):
        x._target_filename_valid()

@pytest.mark.rule
def test_source_is_precedented_ok():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    x._source_is_precedented()
    y = Rule('1', 'LATER', 'b.txt', 'c.txt', '0')
    assert y._source_is_precedented

@pytest.mark.rule
def test_source_is_precedented_not():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    x._source_is_precedented()
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    with pytest.raises(SystemExit):
        y._source_is_precedented()

@pytest.mark.rule
def test_source_matchfield_is_integer():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_is_integer

@pytest.mark.rule
def test_target_sortorder_is_integer():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._target_sortorder_is_integer

@pytest.mark.rule
def test_source_ne_target():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_not_equal_target

@pytest.mark.rule
def test_source_ne_target_not():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_not_equal_target()

@pytest.mark.rule
def test_source_matchpattern_is_valid():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    assert x._source_matchpattern_is_valid

@pytest.mark.rule
def test_source_matchpattern_is_valid_not():
    x = Rule('1', 'N(OW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()
