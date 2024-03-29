"""Returns True if line (or part of line) matches a given regular expression."""

from mklists.booleans import dataline_matches_ruleobj
from mklists.rules import Rule


def test_dataline_matches_ruleobj():
    """Returns True: matches simple regex in field 1."""
    rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    line = "NOW Buy milk"
    assert dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)


def test_dataline_matches_ruleobj_with_space():
    """Returns True: matches regex in field 1, despite leading whitespace."""
    rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    line = " NOW Buy milk"
    assert dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)


def test_dataline_matches_ruleobj_no_match():
    """Returns False: does not match simple regex in field 1."""
    rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    line = "LATER Buy milk"
    assert not dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)


def test_dataline_matches_ruleobj_gotcha():
    """Returns True despite the leading whitespace in the line
    because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']."""
    rule = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    line = " NOW Buy milk"
    assert dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)


def test_dataline_matches_ruleobj_entire_line():
    """Returns True because regex matches the start of the entire line."""
    rule = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    line = "NOW Buy milk"
    assert dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)


def test_dataline_matches_ruleobj_entire_line_escaping_parenthesis():
    """Returns True because regex matches the start of the entire line."""
    # pylint: disable=anomalous-backslash-in-string
    # Thank you for catching this, Pylint, but the mistake is intentional...
    rule = Rule(0, "^N\(OW", "a.txt", "b.txt", 0)
    assert dataline_matches_ruleobj(ruleobj=rule, dataline_str="N(OW Buy milk")


def test_dataline_matches_ruleobj_no_match_when_line_has_less_fields_than_rule():
    """Returns False because line does not have six fields."""
    rule = Rule(6, "^NOW", "a.txt", "b.txt", 0)
    line = "NOW Buy milk"
    assert not dataline_matches_ruleobj(ruleobj=rule, dataline_str=line)
