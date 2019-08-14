"""Tests for run.py

Note that function seems to work regardless of whether values
are passed as positional or keyword arguments.
"""

from mklists.booleans import is_match_to_rule_as_line
from mklists.rules import Rule


def test_apply_is_match_to_rule_as_line():
    """@@@Docstring"""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_match_to_rule_as_line(given_ruleobj, "NOW Buy milk") is True


def test_apply_is_match_to_rule_as_line_with_space():
    """@@@Docstring"""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_match_to_rule_as_line(given_ruleobj, " NOW Buy milk") is True


def test_apply_is_match_to_rule_as_line_no_match():
    """@@@Docstring"""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_match_to_rule_as_line(given_ruleobj, "LATER Buy milk") is False


def test_apply_is_match_to_rule_as_line_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    given_ruleobj = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    is_match_to_rule_as_line(given_ruleobj, " NOW Buy milk") is True


def test_apply_is_match_to_rule_as_line_entire_line():
    """@@@Docstring"""
    given_ruleobj = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    is_match_to_rule_as_line(given_ruleobj, "NOW Buy milk") is True
