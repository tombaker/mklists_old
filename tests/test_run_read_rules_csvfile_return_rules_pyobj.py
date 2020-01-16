"""@@@Docstring"""

import io
import os
import pytest

from mklists.config import RULES_CSVFILE_NAME
from mklists.exceptions import NoRulefileError, NoRulesError
from mklists.run import read_rules_csvfile_return_rules_pyobj

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR = (
    "0|.|x|lines|0|A comment\n"
    "1|NOW|lines|alines|1|Another comment\n"
    "1|LATER|lines|alines|1|\n"
    "0|^2019 ..|lines|blines|1|\n"
)

TEST_RULES_CSVSTR_RN = (
    "0|.|x|lines|0|A comment\r\n"
    "1|NOW|lines|alines|1|Another comment\r\n"
    "1|LATER|lines|alines|1|\r\n"
    "0|^2019 ..|lines|blines|1|\r\n"
)

TEST_RULES_CSVSTR_WITH_NOISE = (
    "0|.|x|lines|0|A comment\n"
    "1|NOW|lines|alines|1|Another comment\n"
    "1|LATER|lines|alines|1|\n"
    "0|^2019 ..|lines|blines|1|\n"
    "_|^2019 ..|lines|blines|1|Line starts with non-integer\n"
    "0|^2019 ..|lines|Line is too short\n"
    "\n"
    "0|^2019 ..|lines|clines|2|Line does not end with newline"
)

TEST_RULES_CSVSTR_WITH_HEADERS = (
    "source_matchfield|source_matchpattern|source|target|target_sortorder\n"
    "0|.|x|lines|0|A comment\n"
    "1|NOW|lines|alines|1|Another comment\n"
    "1|LATER|lines|alines|1|\n"
    "0|^2019 ..|lines|blines|1|\n"
)


PYOBJ = [
    ["0", ".", "x", "lines", "0"],
    ["1", "NOW", "lines", "alines", "1"],
    ["1", "LATER", "lines", "alines", "1"],
    ["0", "^2019 ..", "lines", "blines", "1"],
]

TEST_RULES_CSVSTR_RN = "source_matchfield|source_matchpattern|source|target|target_sortorder\r\n0|.|x|lines|0\r\n1|NOW|lines|alines|1\r\n1|LATER|lines|alines|1\r\n0|^2019|^2020|lines|blines|1"


@pytest.mark.csvrules
def test_read_rules_csvfile_return_rules_pyobj(tmpdir):
    """Fine if CSV file has no header line because it will be ignored anyway."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = read_rules_csvfile_return_rules_pyobj(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_no_rules(tmpdir):
    """Exits with NoRulefileError if called without specifying a CSV file."""
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj(csvfile=None)


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj(tmpdir):
    """The CSV file may have a header line, though it will be ignored."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = read_rules_csvfile_return_rules_pyobj(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


@pytest.mark.skip
@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_rn(tmpdir):
    """The "CSV file" may have MS-Windows line endings (\r\n)."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_RN)
    assert (
        read_rules_csvfile_return_rules_pyobj(RULES_CSVFILE_NAME)
        == TEST_RULES_CSVSTR_RN
    )


@pytest.mark.skip
@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_not_specified(tmpdir):
    """Function must be called with one argument (name of the "CSV file")."""
    # 2019-09-30: Problem has something to do with testing for
    # wrong exception raised
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj()


@pytest.mark.skip
@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_not_found(tmpdir):
    """Function raises exception if "CSV file" is not found."""
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj(csvfile=None)
