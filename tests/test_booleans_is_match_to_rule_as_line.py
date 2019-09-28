"""Returns True if line (or part of line) matches a given regular expression."""

import pytest
from mklists.booleans import line_is_match_to_rule
from mklists.rules import Rule


def test_line_is_match_to_rule():
    """Returns True: matches simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "NOW Buy milk"
    assert line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_line_is_match_to_rule_with_space():
    """Returns True: matches regex in field 1, despite leading whitespace."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = " NOW Buy milk"
    assert line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_line_is_match_to_rule_no_match():
    """Returns False: does not match simple regex in field 1."""
    given_ruleobj = Rule(1, "NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "LATER Buy milk"
    assert not line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


def test_line_is_match_to_rule_gotcha():
    """Returns True despite the leading whitespace in the line
    because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']."""
    given_ruleobj = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    given_dataline_str = " NOW Buy milk"
    assert line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


@pytest.mark.improve
def test_line_is_match_to_rule_entire_line():
    """Returns True because regex matches the start of the entire line."""
    given_ruleobj = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    given_dataline_str = "NOW Buy milk"
    assert line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
    )


@pytest.mark.improve
@pytest.mark.skip
def test_line_is_match_to_rule_does_not_match_if_regex_is_bad():
    """Raises exception because regex is bad.
    The function line_is_match_to_rule() does not test validity of the
    regex - this is done by the Rule method _source_matchpattern_is_valid()."""
    given_ruleobj = Rule(0, "^N(OW", "a.txt", "b.txt", 0)
    given_dataline_str = "N(OW Buy milk"
    with pytest.raises(SystemExit):
        line_is_match_to_rule(
            _given_ruleobj=given_ruleobj, _given_dataline_str=given_dataline_str
        )


def test_line_is_match_to_rule_entire_line_escaping_parenthesis():
    """Returns True because regex matches the start of the entire line."""
    given_ruleobj = Rule(0, "^N\(OW", "a.txt", "b.txt", 0)
    assert line_is_match_to_rule(
        _given_ruleobj=given_ruleobj, _given_dataline_str="N(OW Buy milk"
    )
