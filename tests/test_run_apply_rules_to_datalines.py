"""Tests for run.py"""

import pytest
from mklists.run import apply_rules_to_datalines
from mklists.rules import Rule


def test_apply_rules_to_datalines_no_rules_specified():
    """Not passing rules to apply_rules_to_datalines raises SystemExit."""
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(dataline_list=[["a line\n"]])


def test_apply_rules_to_datalines_no_rules_specified_either():
    rules = []
    lines = ["NOW Summer\n", "LATER Winter\n"]
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)


def test_apply_rules_to_datalines_no_data_specified():
    """Not passing data to apply_rules_to_datalines raises SystemExit."""
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(ruleobj_list=[[Rule(1, "a", "b", "c", 2)]])


def test_apply_rules_to_datalines_no_data_specified_either():
    rules = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    lines = []
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)


def test_apply_rules_to_datalines_correct_result():
    """apply_rules_to_datalines works as it should."""
    rules = [Rule(0, "i", "a.txt", "b.txt", 0)]
    lines = ["two ticks\n", "an ant\n", "the mite\n"]
    mdict = {"a.txt": ["an ant\n"], "b.txt": ["two ticks\n", "the mite\n"]}
    apply_rules_to_datalines(rules, lines) == mdict


def test_apply_rules_to_datalines_another_correct_result():
    rules = [Rule(2, "i", "a.txt", "b.txt", 1)]
    lines = ["two ticks\n", "an ant\n", "the mite\n"]
    mdict = {"a.txt": ["an ant\n"], "b.txt": ["the mite\n", "two ticks\n"]}
    apply_rules_to_datalines(rules, lines) == mdict


def test_apply_rules_to_datalines_yet_another_correct_result():
    rules = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    lines = ["NOW Summer\n", "LATER Winter\n"]
    mdict = {"now.txt": ["NOW Summer\n"], "later.txt": ["LATER Winter\n"], "a.txt": []}
    apply_rules_to_datalines(rules, lines) == mdict


def test_apply_rules_to_datalines_correct_result_too():
    rules = [Rule(1, ".", "a.txt", "now.txt", 1)]
    lines = ["LATER Winter\n", "NOW Summer\n"]
    mdict = {"now.txt": ["NOW Summer\n", "LATER Winter\n"], "a.txt": []}
    apply_rules_to_datalines(rules, lines) == mdict