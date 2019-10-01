"""Returns True if line (or part of line) matches a given regular expression."""

import pytest
from mklists.booleans import dataline_is_match_to_ruleobj
from mklists.rules import Rule


def test_dataline_is_match_to_ruleobj():
    """Returns True: matches simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "NOW Buy milk"
    assert dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_dataline_is_match_to_ruleobj_with_space():
    """Returns True: matches regex in field 1, despite leading whitespace."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = " NOW Buy milk"
    assert dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_dataline_is_match_to_ruleobj_no_match():
    """Returns False: does not match simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "LATER Buy milk"
    assert not dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_dataline_is_match_to_ruleobj_gotcha():
    """Returns True despite the leading whitespace in the line
    because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']."""
    given_ruleobj = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    given_dataline_str = " NOW Buy milk"
    assert dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


@pytest.mark.improve
def test_dataline_is_match_to_ruleobj_entire_line():
    """Returns True because regex matches the start of the entire line."""
    given_ruleobj = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "NOW Buy milk"
    assert dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_dataline_is_match_to_ruleobj_entire_line_escaping_parenthesis():
    """Returns True because regex matches the start of the entire line."""
    given_ruleobj = Rule(0, "^N\(OW", "a.txt", "b.txt", 0)
    assert dataline_is_match_to_ruleobj(
        _given_ruleobj=given_ruleobj, _given_dataline_str="N(OW Buy milk"
    )
