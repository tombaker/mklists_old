"""Tests for run.py"""

from mklists.utils import is_line_match_to_rule
from mklists.rules import Rule


def test_apply_is_line_match_to_rule():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_rule, "NOW Buy milk") is True


def test_apply_is_line_match_to_rule_with_space():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_rule, " NOW Buy milk") is True


def test_apply_is_line_match_to_rule_no_match():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_rule, "LATER Buy milk") is False


def test_apply_is_line_match_to_rule_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    given_rule = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_rule, " NOW Buy milk") is True


def test_apply_is_line_match_to_rule_entire_line():
    given_rule = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    is_line_match_to_rule(given_rule, "NOW Buy milk") is True