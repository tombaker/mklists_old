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
    "1|NOW|lines|alines|1|The following line is blank\n"
    "\n"
    "1|LATER|lines|alines|1|\n"
    "0|^2019 ..|lines|blines|1|List does not end with newline"
    "_|^2018 ..|lines|blines|1|Line starts with non-integer\n"
    "0|^2017 ..|lines|Line is too short\n"
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


@pytest.mark.csvrules
def test_read_rules_csvfile_return_rules_pyobj(tmpdir):
    """Fine if CSV file has no header line because it will be ignored anyway."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = read_rules_csvfile_return_rules_pyobj(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj(tmpdir):
    """The CSV file may have a header line, though it will be ignored."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = read_rules_csvfile_return_rules_pyobj(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_rn(tmpdir):
    """Fine for CSV file to have MS-Windows line endings (\r\n)."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_RN)
    expected = PYOBJ
    real = read_rules_csvfile_return_rules_pyobj(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_rulefile_not_specified(tmpdir):
    """Raises NoRulefileError if specified CSV file is "None"."""
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj(csvfile=None)


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_rulefile_not_specified2(tmpdir):
    """Raises NoRulefileError if called specifying no argument at all."""
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj()


@pytest.mark.csvrules
def test_run_read_rules_csvfile_return_rules_pyobj_not_found(tmpdir):
    """Raises NoRulefileError if specified CSV file is not found."""
    os.chdir(tmpdir)
    tmpdir.join(".rules2").write(TEST_RULES_CSVSTR)
    with pytest.raises(NoRulefileError):
        read_rules_csvfile_return_rules_pyobj(csvfile=".rules3")
