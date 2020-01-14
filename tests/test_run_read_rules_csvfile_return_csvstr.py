"""@@@Docstring"""

import io
import os
import pytest

from mklists.config import RULES_CSVFILE_NAME
from mklists.exceptions import NoRulefileError
from mklists.run import read_rules_csvfile_return_csvstr

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR = "source_matchfield|source_matchpattern|source|target|target_sortorder\n0|.|x|lines|0\n1|NOW|lines|alines|1\n1|LATER|lines|alines|1\n0|^2019|^2020|lines|blines|1"

TEST_RULES_CSVSTR_HEADLESS = "0|.|x|lines|0\n1|NOW|lines|alines|1\n1|LATER|lines|alines|1\n0|^2019|^2020|lines|blines|1"

BINKY = "Binky\nBinky"

TEST_RULES_CSVSTR_RN = "source_matchfield|source_matchpattern|source|target|target_sortorder\r\n0|.|x|lines|0\r\n1|NOW|lines|alines|1\r\n1|LATER|lines|alines|1\r\n0|^2019|^2020|lines|blines|1"


def test_run_read_rules_csvfile_return_csvstr(tmpdir):
    """The "CSV file" may have a header line."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    assert read_rules_csvfile_return_csvstr(RULES_CSVFILE_NAME) == TEST_RULES_CSVSTR


def test_run_read_rules_csvfile_return_csvstr_headless(tmpdir):
    """Okay if the "CSV file" does not have a header line."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_HEADLESS)
    assert (
        read_rules_csvfile_return_csvstr(RULES_CSVFILE_NAME)
        == TEST_RULES_CSVSTR_HEADLESS
    )


def test_run_read_rules_csvfile_return_csvstr_binky(tmpdir):
    """The content of "CSV file" is not tested for validity as CSV."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(BINKY)
    assert read_rules_csvfile_return_csvstr(RULES_CSVFILE_NAME) == BINKY


def test_run_read_rules_csvfile_return_csvstr_rn(tmpdir):
    """The "CSV file" may have MS-Windows line endings (\r\n)."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_RN)
    assert read_rules_csvfile_return_csvstr(RULES_CSVFILE_NAME) == TEST_RULES_CSVSTR_RN


def test_run_read_rules_csvfile_return_csvstr_not_specified(tmpdir):
    """Function must be called with one argument (name of the "CSV file")."""
    # 2019-09-30: Problem has something to do with testing for
    # wrong exception raised
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_csvstr()


def test_run_read_rules_csvfile_return_csvstr_not_found(tmpdir):
    """Function raises exception if "CSV file" is not found."""
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_csvstr(csvfile=None)
