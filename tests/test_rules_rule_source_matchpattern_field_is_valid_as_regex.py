"""Some rule module tests use temporary directory fixture."""

import pytest
from mklists.rules import Rule


def test_rule_source_matchpattern_field_is_valid_as_regex():
    """Regex in rule object is valid."""
    rule_obj = Rule("1", "NOW", "a.txt", "a.txt", "0")
    assert rule_obj._source_matchpattern_field_is_valid_as_regex


def test_rule_source_matchpattern_is_not_valid():
    """Regex in rule object is bad, raises SystemExit."""
    rule_obj = Rule("1", "N(OW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        rule_obj._source_matchpattern_field_is_valid_as_regex()


def test_rule_field_source_matchpattern_regex_has_space():
    """Second field of Rule object, a regex, has an allowable space."""
    rule_obj = Rule(1, "^X 19", "a", "b", 2)
    assert rule_obj.source_matchpattern == "^X 19"
