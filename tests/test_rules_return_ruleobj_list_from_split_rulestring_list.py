"""
run.py: return_ruleobj_list_from_rulefile_chain
    Return list of rule objects from configuration and rule files.
"""

import io
import os
import pytest
from mklists.exceptions import NoRulesError
from mklists.rules import Rule, return_ruleobj_list_from_split_rulestring_list
from mklists.constants import RULE_YAMLFILE_NAME

TEST_RULES_YAMLFILE_STR = r"""# Test rules for this module only.
- [0, '.',          x,         lines,            0]
- [1, 'NOW',        lines,     alines,           1]
- [1, 'LATER',      lines,     alines,           1]
- [0, '^2019|2020', lines,     blines,           1]"""

TEST_RULES_YAMLFILE_SPLIT = [
    [0, ".", "x", "lines", 0],
    [1, "NOW", "lines", "alines", 1],
    [1, "LATER", "lines", "alines", 1],
    [0, "^2019|2020", "lines", "blines", 1],
]

TEST_RULEOBJ_LIST = [
    Rule(
        source_matchfield=0,
        source_matchpattern=".",
        source="x",
        target="lines",
        target_sortorder=0,
    ),
    Rule(
        source_matchfield=1,
        source_matchpattern="NOW",
        source="lines",
        target="alines",
        target_sortorder=1,
    ),
    Rule(
        source_matchfield=1,
        source_matchpattern="LATER",
        source="lines",
        target="alines",
        target_sortorder=1,
    ),
    Rule(
        source_matchfield=0,
        source_matchpattern="^2019|2020",
        source="lines",
        target="blines",
        target_sortorder=1,
    ),
]


@pytest.mark.now
def test_run_return_ruleobj_list_from_split_rulestring_list(tmpdir):
    """@@@Docstring"""
    expected = TEST_RULEOBJ_LIST
    real = return_ruleobj_list_from_split_rulestring_list(
        _split_rulestring_list=TEST_RULES_YAMLFILE_SPLIT
    )
    assert real == expected


@pytest.mark.now
def test_run_return_ruleobj_list_from_split_rulestring_list_no_rules(tmpdir):
    """@@@Docstring"""
    with pytest.raises(NoRulesError):
        return_ruleobj_list_from_split_rulestring_list(_split_rulestring_list=[])
