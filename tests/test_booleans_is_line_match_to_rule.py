"""Tests for run.py

Note that function seems to work regardless of whether values
are passed as positional or keyword arguments.
"""

from mklists.booleans import is_line_match_to_rule
from mklists.rules import Rule


def test_apply_is_line_match_to_rule():
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_ruleobj, "NOW Buy milk") is True


def test_apply_is_line_match_to_rule_with_space():
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_ruleobj, " NOW Buy milk") is True


def test_apply_is_line_match_to_rule_no_match():
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_ruleobj, "LATER Buy milk") is False


def test_apply_is_line_match_to_rule_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    given_ruleobj = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_ruleobj, " NOW Buy milk") is True


def test_apply_is_line_match_to_rule_entire_line():
    given_ruleobj = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_ruleobj, "NOW Buy milk") is True
