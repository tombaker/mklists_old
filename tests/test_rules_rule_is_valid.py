"""Some rule module tests use temporary directory fixture."""

import pytest
from mklists.rules import Rule


def test_rule_is_valid(reinitialize_ruleclass_variables):
    """A well-formed rule object is valid."""
    rule_instance = Rule(1, "NOW", "a.txt", "b.txt", 2)
    assert rule_instance.is_valid()


def test_rule_is_valid_number_fields_are_integers(reinitialize_ruleclass_variables):
    """First and last fields of rule object are integers."""
    rule_instance = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert rule_instance.is_valid()


def test_rule_is_valid_number_fields_are_integers_too(reinitialize_ruleclass_variables):
    """Rule object is valid even if initialized with string integers."""
    rule_instance = Rule("1", "NOW", "a.txt", "b.txt", "2")
    assert rule_instance.is_valid()


def test_rule_source_matchpattern_is_not_valid_too(reinitialize_ruleclass_variables):
    """Rule object fails self-validation because regex is bad."""
    rule_instance = Rule(1, "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_instance.is_valid()


def test_rule_source_not_initialized(reinitialize_ruleclass_variables):
    """Rule object was initialized with 'source' of first rule."""
    rule_instance = Rule(1, "NOW", "a.txt", "b.txt", 0)
    rule_instance.is_valid()
    rule_instance2 = Rule(1, "LATER", "b.txt", "c.txt", 0)
    assert rule_instance2.is_valid()


def test_rule_source_not_initialized_too(reinitialize_ruleclass_variables):
    """Rule object correctly initialized sources from multiple rules."""
    rule_instance = Rule(1, "NOW", "a.txt", "b.txt", 0)
    rule_instance.is_valid()
    rule_instance2 = Rule(1, "LATER", "b.txt", "c.txt", 0)
    rule_instance2.is_valid()
    sources = ["a.txt", "b.txt", "c.txt"]
    assert Rule.sources_list == sources


def test_rule_source_not_initialized_unprecedented(reinitialize_ruleclass_variables):
    """Rule class keeps track of instances registered, so
    second rule instance 'y' should raise exception because
    'c.txt' will not have been registered as a source."""
    rule_instance = Rule("1", "NOW", "a.txt", "b.txt", "0")
    rule_instance.is_valid()
    rule_instance2 = Rule("1", "LATER", "c.txt", "d.txt", "0")
    with pytest.raises(SystemExit):
        rule_instance2.is_valid()
