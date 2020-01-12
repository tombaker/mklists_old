"""@@@Docstring"""

import io
import os
import pytest

# from mklists.constants import RULE_CSVFILE_NAME
from mklists.exceptions import NoRulesError
from mklists.rules import Rule, return_ruleobj_list_from_yamlstr
from mklists.utils import return_pyobj_from_yamlstr

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_YAMLSTR = r"""# Test rules for this module only.
- [0, '.',          x,         lines,            0]
- [1, 'NOW',        lines,     alines,           1]
- [1, 'LATER',      lines,     alines,           1]
- [0, '^2019|^2020', lines,     blines,           1]"""

TEST_RULES_YAMLSTR_PARSED = [
    [0, ".", "x", "lines", 0],
    [1, "NOW", "lines", "alines", 1],
    [1, "LATER", "lines", "alines", 1],
    [0, "^2019|^2020", "lines", "blines", 1],
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
        source_matchpattern="^2019|^2020",
        source="lines",
        target="blines",
        target_sortorder=1,
    ),
]


def test_run_return_ruleobj_list_from_yamlstr(tmpdir):
    """@@@Docstring"""
    expected = TEST_RULEOBJ_LIST
    real = return_ruleobj_list_from_yamlstr(yamlstr=TEST_RULES_YAMLSTR)
    assert real == expected


def test_run_return_ruleobj_list_from_yamlstr_no_rules(tmpdir):
    """@@@Docstring"""
    # 2019-09-30: Problem has something to do with testing for
    # wrong exception raised
    with pytest.raises(NoRulesError):
        return_ruleobj_list_from_yamlstr(yamlstr=None)
