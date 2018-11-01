"""Some rule module tests use temporary directory fixture."""

import os
import pytest
from mklists.rules import Rule, apply_rules_to_datalines, _line_matches
from mklists import UninitializedSourceError, BUILTIN_GRULES
from mklists.readwrite import (write_yamlstr_to_yamlfile, 
    read_yamlfile_return_pyobject)


@pytest.mark.yaml
def test_write_yamlstr(tmpdir):
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules', lrules_yamlstr)
    some_yamlstr = open('_lrules').read()
    assert lrules_yamlstr == some_yamlstr

@pytest.mark.yaml
def test_read_good_yamlfile(tmpdir):
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules', lrules_yamlstr)
    pyobject = read_yamlfile_return_pyobject('_lrules')
    good_pyobject = [[1, 'NOW', 'a', 'b', 0], [1, 'LATER', 'a', 'c', 0]]
    assert pyobject == good_pyobject

@pytest.mark.yaml
def test_read_bad_yamlfile(tmpdir):
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules_bad', bad_yamlstr)
    with pytest.raises(SystemExit):
        read_yamlfile_return_pyobject('_lrules_bad')


@pytest.mark.rule
def test_no_rules_specified():
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(datalines_list=[["a line\n"]])


@pytest.mark.rule
def test_no_data_specified():
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(ruleobjs_list=[[Rule(1, "a", "b", "c", 2)]])


@pytest.mark.rule
def test_rule_is_valid(reinitialize_ruleclass_variables):
    x = Rule(1, "NOW", "a.txt", "b.txt", 2)
    assert x.is_valid()


@pytest.mark.rule
def test_rule_is_valid_even_with_integer_strings(
    reinitialize_ruleclass_variables
):
    x = Rule("1", "NOW", "a.txt", "b.txt", "2")
    assert x.is_valid()


@pytest.mark.rule
def test_number_fields_are_integers(reinitialize_ruleclass_variables):
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert x.is_valid()


@pytest.mark.rule
def test_rule_has_string_where_integer_required(
    reinitialize_ruleclass_variables
):
    x = Rule("1", "N(OW", "a", "b", 2)
    assert x._number_fields_are_integers() == 1


@pytest.mark.rule
def test_source_was_previously_declared(reinitialize_ruleclass_variables):
    x = Rule(1, "NOW", "a.txt", "b.txt", 0)
    x.is_valid()
    y = Rule(1, "LATER", "b.txt", "c.txt", 0)
    assert y.is_valid()


@pytest.mark.rule
def test_sources_list(reinitialize_ruleclass_variables):
    x = Rule(1, "NOW", "a.txt", "b.txt", 0)
    x.is_valid()
    y = Rule(1, "LATER", "b.txt", "c.txt", 0)
    y.is_valid()
    sources = ["a.txt", "b.txt", "c.txt"]
    assert Rule.sources_list == sources


@pytest.mark.rule
def test_source_is_not_precedented(reinitialize_ruleclass_variables):
    """Rule class keeps track of instances registered, so 
    second rule instance 'y' should raise exception because 
    'c.txt' will not have been registered as a source."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    x.is_valid()
    y = Rule("1", "LATER", "c.txt", "d.txt", "0")
    with pytest.raises(SystemExit):
        y.is_valid()


@pytest.mark.rule
def test_rule_is_not_valid(reinitialize_ruleclass_variables):
    x = Rule(1, "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        x.is_valid()


@pytest.mark.rule
def test_rule():
    x = Rule(1, ".", "a", "b", 2)
    assert x.source == "a"


@pytest.mark.rule
def test_rulestring_regex_has_space():
    x = Rule(1, "^X 19", "a", "b", 2)
    assert x.source_matchpattern == "^X 19"


@pytest.mark.rule
def test_source_filename_valid():
    x = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert x._filenames_are_valid()


@pytest.mark.rule
def test_target_filename_valid():
    x = Rule(1, "^X 19", "a.txt", "b.txt", 2)
    assert x._filenames_are_valid()


@pytest.mark.rule
def test_target_filename_not_valid():
    x = Rule(1, "^X 19", "a.txt", "b^.txt", 2)
    with pytest.raises(SystemExit):
        x._filenames_are_valid()


@pytest.mark.rule
def test_source_ne_target():
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert x._source_is_not_equal_target


@pytest.mark.rule
def test_source_equals_target_oops():
    x = Rule("1", "NOW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        x._source_is_not_equal_target()


@pytest.mark.rule
def test_source_matchpattern_is_valid():
    x = Rule("1", "NOW", "a.txt", "a.txt", "0")
    assert x._source_matchpattern_is_valid


@pytest.mark.rule
def test_source_matchpattern_is_not_valid():
    x = Rule("1", "N(OW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()


@pytest.mark.apply_rules
def test_apply_rules():
    rules = [Rule(0, "i", "a.txt", "b.txt", 0)]
    lines = ["two ticks\n", "an ant\n", "the mite\n"]
    mdict = {"a.txt": ["an ant\n"], "b.txt": ["two ticks\n", "the mite\n"]}
    apply_rules_to_datalines(rules, lines) == mdict


@pytest.mark.apply_rules
def test_apply_rules2():
    rules = [Rule(2, "i", "a.txt", "b.txt", 1)]
    lines = ["two ticks\n", "an ant\n", "the mite\n"]
    mdict = {"a.txt": ["an ant\n"], "b.txt": ["the mite\n", "two ticks\n"]}
    apply_rules_to_datalines(rules, lines) == mdict


@pytest.mark.apply_rules
def test_apply_rules3():
    rules = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    lines = ["NOW Summer\n", "LATER Winter\n"]
    mdict = {
        "now.txt": ["NOW Summer\n"],
        "later.txt": ["LATER Winter\n"],
        "a.txt": [],
    }
    apply_rules_to_datalines(rules, lines) == mdict


@pytest.mark.apply_rules
def test_apply_rules_no_data():
    rules = [
        Rule(1, "NOW", "a.txt", "now.txt", 0),
        Rule(1, "LATER", "a.txt", "later.txt", 0),
    ]
    lines = []
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)


@pytest.mark.apply_rules
def test_apply_rules_no_rules():
    rules = []
    lines = ["NOW Summer\n", "LATER Winter\n"]
    with pytest.raises(SystemExit):
        apply_rules_to_datalines(rules, lines)


@pytest.mark.apply_rules
def test_apply_rules_sorted():
    rules = [Rule(1, ".", "a.txt", "now.txt", 1)]
    lines = ["LATER Winter\n", "NOW Summer\n"]
    mdict = {"now.txt": ["NOW Summer\n", "LATER Winter\n"], "a.txt": []}
    apply_rules_to_datalines(rules, lines) == mdict


@pytest.mark.line_matches
def test_line_matches():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    _line_matches(given_rule, "NOW Buy milk") == True


@pytest.mark.line_matches
def test_line_matches_with_space():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    _line_matches(given_rule, " NOW Buy milk") == True


@pytest.mark.line_matches
def test_line_matches_no_match():
    given_rule = Rule(1, "NOW", "a.txt", "b.txt", 0)
    _line_matches(given_rule, "LATER Buy milk") == False


@pytest.mark.line_matches
def test_line_matches_gotcha():
    """True because ' NOW Buy milk'.split() => ['NOW', 'Buy', 'milk']"""
    given_rule = Rule(1, "^NOW", "a.txt", "b.txt", 0)
    _line_matches(given_rule, " NOW Buy milk") == True


@pytest.mark.line_matches
def test_line_matches_entire_line():
    given_rule = Rule(0, "^NOW", "a.txt", "b.txt", 0)
    _line_matches(given_rule, "NOW Buy milk") == True
