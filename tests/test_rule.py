import pytest
from mklists.rule import Rule

@pytest.mark.skip
def test_source_is_registered():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    Rule.register(x)
    y = Rule('1', 'LATER', 'b.txt', 'c.txt', '0')
    assert Rule.register(y)

@pytest.mark.skip
def test_source_is_registered_not():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    Rule.register(x)
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    with pytest.raises(SystemExit):
        Rule.register(y)

@pytest.mark.rule
def test_is_valid_not():
    x = Rule(1, 'N(OW', 'a', 'b', 2)
    with pytest.raises(SystemExit):
        x.is_valid()

@pytest.mark.rule
def test_rule():
    x = Rule(1, '.', 'a', 'b', 2)
    assert x.source == 'a'

@pytest.mark.rule
def test_rulestring_regex_has_space():
    x = Rule(1, '^X 19', 'a', 'b', 2)
    assert x.source_matchpattern == '^X 19'

@pytest.mark.rule
def test_source_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._source_and_target_filenames_are_valid()

@pytest.mark.rule
def test_target_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._source_and_target_filenames_are_valid()

@pytest.mark.rule
def test_target_filename_valid_not():
    x = Rule('1', '^X 19', 'a.txt', 'b^.txt', '2')
    with pytest.raises(SystemExit):
        x._source_and_target_filenames_are_valid()

@pytest.mark.rule
def test_source_matchfield_and_target_sortorder_are_valid():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_and_target_sortorder_are_integers

@pytest.mark.rule
def test_source_matchfield_and_target_sortorder_are_integers():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_and_target_sortorder_are_integers

@pytest.mark.rule
def test_source_ne_target():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_is_not_equal_target

@pytest.mark.rule
def test_source_ne_target_not():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_is_not_equal_target()

@pytest.mark.rule
def test_source_matchpattern_is_valid():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    assert x._source_matchpattern_is_valid

@pytest.mark.rule
def test_source_matchpattern_is_valid_not():
    x = Rule('1', 'N(OW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()
