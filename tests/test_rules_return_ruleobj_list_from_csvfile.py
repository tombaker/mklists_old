"""@@@Docstring"""

import io
import os
import pytest

from mklists.exceptions import NoRulefileError
from mklists.rules import Rule, return_ruleobj_list_from_csvfile

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR = "source_matchfield,source_matchpattern,source,target,target_sortorder\n0,.,x,lines,0\n1,NOW,lines,alines,1\n1,LATER,lines,alines,1\n0,^2019|^2020,lines,blines,1"

TEST_RULES_CSVSTR_RN = "source_matchfield,source_matchpattern,source,target,target_sortorder\r\n0,.,x,lines,0\r\n1,NOW,lines,alines,1\r\n1,LATER,lines,alines,1\r\n0,^2019|^2020,lines,blines,1"


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


@pytest.mark.csv
def test_run_return_ruleobj_list_from_csvfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    tmpdir.join("rules.csv").write(TEST_RULES_CSVSTR)
    expected = TEST_RULEOBJ_LIST
    real = return_ruleobj_list_from_csvfile(filename="rules.csv")
    assert real == expected


@pytest.mark.csv
def test_run_return_ruleobj_list_from_csvfile_rulefile_not_specified(tmpdir):
    """@@@Docstring"""
    # 2019-09-30: Problem has something to do with testing for
    # wrong exception raised
    with pytest.raises(NoRulefileError):
        return_ruleobj_list_from_csvfile()


@pytest.mark.csv
def test_run_return_ruleobj_list_from_csvfile_rulefile_not_found(tmpdir):
    """@@@Docstring"""
    with pytest.raises(NoRulefileError):
        return_ruleobj_list_from_csvfile(filename=None)
