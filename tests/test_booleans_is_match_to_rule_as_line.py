"""Returns True if line (or part of line) matches a given regular expression."""

from mklists.booleans import is_match_to_rule_as_line
from mklists.rules import Rule


def test_is_match_to_rule_as_line():
    """Returns True: matches simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    assert is_match_to_rule_as_line(given_ruleobj, "NOW Buy milk")


def test_is_match_to_rule_as_line_with_space():
    """Returns True: matches regex in field 1, despite leading whitespace."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    assert is_match_to_rule_as_line(given_ruleobj, " NOW Buy milk")


def test_is_match_to_rule_as_line_no_match():
    """Returns False: does not match simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    assert not is_match_to_rule_as_line(given_ruleobj, "LATER Buy milk")


def test_is_match_to_rule_as_line_gotcha():
    """Returns True despite the leading whitespace in the line
    because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']."""
    given_ruleobj = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    assert is_match_to_rule_as_line(given_ruleobj, " NOW Buy milk")


def test_is_match_to_rule_as_line_entire_line():
    """Returns True because regex matches the start of the entire line."""
    given_ruleobj = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    assert is_match_to_rule_as_line(given_ruleobj, "NOW Buy milk")
