"""Some rule module tests use temporary directory fixture."""

import pytest
from mklists.rules import Rule


def test_rule_is_valid(reinitialize_ruleclass_variables):
    """A well-formed rule object is valid."""
    x = Rule(1, "NOW", "a.txt", "b.txt", 2)
    assert x.is_valid()


def test_rule_is_valid_number_fields_are_integers(reinitialize_ruleclass_variables):
    """First and last fields of rule object are integers."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert x.is_valid()


def test_rule_is_valid_number_fields_are_integers_too(reinitialize_ruleclass_variables):
    """Rule object is valid even if initialized with string integers."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "2")
    assert x.is_valid()


def test_rule_number_fields_are_integers(reinitialize_ruleclass_variables):
    x = Rule("1", "N(OW", "a", "b", 2)
    assert x._number_fields_are_integers() == 1


def test_rule_source_matchpattern_is_valid():
    """Regex in rule object is valid."""
    x = Rule("1", "NOW", "a.txt", "a.txt", "0")
    assert x._source_matchpattern_is_valid


def test_rule_source_matchpattern_is_not_valid():
    """Regex in rule object is bad, raises SystemExit."""
    x = Rule("1", "N(OW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()


def test_rule_source_matchpattern_is_not_valid_too(reinitialize_ruleclass_variables):
    """Rule object fails self-validation because regex is bad."""
    x = Rule(1, "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        x.is_valid()


def test_rule_field_source_matchpattern_regex_has_space():
    """Second field of Rule object, a regex, has an allowable space."""
    x = Rule(1, "^X 19", "a", "b", 2)
    assert x.source_matchpattern == "^X 19"


def test_rule_filenames_are_valid_source_filename_valid():
    """Third field of Rule object ('source') is valid as a filename."""
    x = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert x._filenames_are_valid()


def test_rule_filenames_are_valid_target_filename_valid():
    """Fourth field of Rule object ('target') is valid as a filename."""
    x = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert x._filenames_are_valid()


def test_rule_filenames_are_valid_target_filename_not_valid():
    """Fourth field of Rule object ('target') not valid, raises SystemExit."""
    x = Rule(1, "^X 19", "a.txt", "b^.txt", 2)
    with pytest.raises(SystemExit):
        x._filenames_are_valid()


def test_rule_field_source():
    """Third field of Rule object is 'source'."""
    x = Rule(1, ".", "a", "b", 2)
    assert x.source == "a"


def test_rule_source_is_not_equal_target():
    """Source and target fields of rule object are not equivalent."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert x._source_is_not_equal_target


def test_rule_source_is_not_equal_target_oops():
    """Source and target fields of rule object are same, raises SystemExit."""
    x = Rule("1", "NOW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        x._source_is_not_equal_target()


def test_rule_source_not_initialized(reinitialize_ruleclass_variables):
    """Rule object was initialized with 'source' of first rule."""
    x = Rule(1, "NOW", "a.txt", "b.txt", 0)
    x.is_valid()
    y = Rule(1, "LATER", "b.txt", "c.txt", 0)
    assert y.is_valid()


def test_rule_source_not_initialized_too(reinitialize_ruleclass_variables):
    """Rule object correctly initialized sources from multiple rules."""
    x = Rule(1, "NOW", "a.txt", "b.txt", 0)
    x.is_valid()
    y = Rule(1, "LATER", "b.txt", "c.txt", 0)
    y.is_valid()
    sources = ["a.txt", "b.txt", "c.txt"]
    assert Rule.sources_list == sources


def test_rule_source_not_initialized_unprecedented(reinitialize_ruleclass_variables):
    """Rule class keeps track of instances registered, so
    second rule instance 'y' should raise exception because
    'c.txt' will not have been registered as a source."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    x.is_valid()
    y = Rule("1", "LATER", "c.txt", "d.txt", "0")
    with pytest.raises(SystemExit):
        y.is_valid()
