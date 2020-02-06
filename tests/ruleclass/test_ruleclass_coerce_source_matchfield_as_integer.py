"""Coerce strings of YAML origin to required types."""


import pytest
from mklists.ruleclass import Rule

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


def test_coerce_source_matchfield_as_integer():
    """Field 1 (source_matchfield) must be an integer."""
    rule_obj = Rule(1, "NOW", "a", "b", 2)
    rule_obj._coerce_source_matchfield_as_integer()
    assert isinstance(rule_obj.source_matchfield, int)


def test_coerce_source_matchfield_as_integer_given_good_string():
    """Field 1 (source_matchfield) must be an integer."""
    rule_obj = Rule("1", "NOW", "a", "b", 2)
    rule_obj._coerce_source_matchfield_as_integer()
    assert isinstance(rule_obj.source_matchfield, int)
    assert rule_obj.source_matchfield == 1


def test_coerce_source_matchfield_as_integer_raise_exception_given_bad_string():
    """Field 1 (source_matchfield) must be an integer."""
    rule_obj = Rule("1 2", "NOW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._coerce_source_matchfield_as_integer()


def test_coerce_source_matchfield_as_integer_raise_exception_given_non_integer():
    """Perversely, int(1.2) evaluates to 1, so why not accept it?"""
    rule_obj = Rule(1.2, "NOW", "a", "b", 1.2)
    rule_obj._coerce_source_matchfield_as_integer()
    assert isinstance(rule_obj.source_matchfield, int)
    assert rule_obj.source_matchfield == 1
