"""@@@Docstring"""

import io
import os
import pytest

from mklists.config import RULES_CSVFILE_NAME
from mklists.exceptions import NoRulefileError
from mklists.rules import Rule, _return_rules_csvstr_from_rules_csvfile

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR = "source_matchfield|source_matchpattern|source|target|target_sortorder\n0|.|x|lines|0\n1|NOW|lines|alines|1\n1|LATER|lines|alines|1\n0|^2019|^2020|lines|blines|1"

TEST_RULES_CSVSTR_RN = "source_matchfield|source_matchpattern|source|target|target_sortorder\r\n0|.|x|lines|0\r\n1|NOW|lines|alines|1\r\n1|LATER|lines|alines|1\r\n0|^2019|^2020|lines|blines|1"


def test_run_return_rules_csvstr_from_rules_csvfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    assert (
        _return_rules_csvstr_from_rules_csvfile(RULES_CSVFILE_NAME) == TEST_RULES_CSVSTR
    )


def test_run_return_rules_csvstr_from_rules_csvfile_rn(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_RN)
    assert (
        _return_rules_csvstr_from_rules_csvfile(RULES_CSVFILE_NAME)
        == TEST_RULES_CSVSTR_RN
    )


def test_run_return_rules_csvstr_from_rules_csvfile_not_specified(tmpdir):
    """@@@Docstring"""
    # 2019-09-30: Problem has something to do with testing for
    # wrong exception raised
    with pytest.raises(NoRulefileError):
        _return_rules_csvstr_from_rules_csvfile()


def test_run_return_rules_csvstr_from_rules_csvfile_not_found(tmpdir):
    """@@@Docstring"""
    with pytest.raises(NoRulefileError):
        _return_rules_csvstr_from_rules_csvfile(csvfile=None)
