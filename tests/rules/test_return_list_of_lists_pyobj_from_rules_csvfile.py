"""Reads '.rules', a CSV file, and returns a Python list of five-item lists."""

import io
import os
import pytest

from mklists.constants import RULES_CSVFILE_NAME
from mklists.exceptions import NoRulefileError, NoRulesError
from mklists.rules import return_list_of_lists_pyobj_from_rules_csvfile

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

TEST_RULES_CSVSTR_LEGACY = (
    "0|.|lines|__RENAME__|\n"
    "0|.|tophone|__RENAME__|\n"
    "\n"
    "1|PHONE|__RENAME__|phone|\n"
    "    2|BDAY|phone|phone_bday|\n"
)

PYOBJ_LEGACY = [
    ["0", ".", "lines", "__RENAME__", ""],
    ["0", ".", "tophone", "__RENAME__", ""],
    ["1", "PHONE", "__RENAME__", "phone", ""],
    ["2", "BDAY", "phone", "phone_bday", ""],
]

PYOBJ = [
    ["0", ".", "x", "lines", "0"],
    ["1", "NOW", "lines", "alines", "1"],
    ["1", "LATER", "lines", "alines", "1"],
    ["0", "^2019 ..", "lines", "blines", "1"],
]


def test_return_list_of_lists_pyobj_from_rules_csvfile(tmpdir):
    """Fine if CSV file has no header line because it will be ignored anyway."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = return_list_of_lists_pyobj_from_rules_csvfile(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


def test_return_list_of_lists_pyobj_from_rules_csvfile_header_ignored(tmpdir):
    """The CSV file may have a header line, though it will be ignored."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = return_list_of_lists_pyobj_from_rules_csvfile(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


def test_return_list_of_lists_pyobj_from_rules_csvfile_rn(tmpdir):
    """Fine for CSV file to have MS-Windows line endings (\r\n)."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_RN)
    expected = PYOBJ
    real = return_list_of_lists_pyobj_from_rules_csvfile(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


def test_return_list_of_lists_pyobj_from_rules_csvfile_legacy(tmpdir):
    """Fine for CSV line to pad fields with spaces and leave field 5 blank."""
    os.chdir(tmpdir)
    tmpdir.join(RULES_CSVFILE_NAME).write(TEST_RULES_CSVSTR_LEGACY)
    expected = PYOBJ_LEGACY
    real = return_list_of_lists_pyobj_from_rules_csvfile(csvfile=RULES_CSVFILE_NAME)
    assert real == expected


def test_return_list_of_lists_pyobj_from_rules_csvfile_rulefile_not_specified(tmpdir):
    """Raises NoRulefileError if specified CSV file is "None"."""
    with pytest.raises(NoRulefileError):
        return_list_of_lists_pyobj_from_rules_csvfile(csvfile=None)


def test_return_list_of_lists_pyobj_from_rules_csvfile_rulefile_not_specified2(tmpdir):
    """Raises NoRulefileError if called specifying no argument at all."""
    with pytest.raises(NoRulefileError):
        return_list_of_lists_pyobj_from_rules_csvfile()


def test_return_list_of_lists_pyobj_from_rules_csvfile_not_found(tmpdir):
    """Raises NoRulefileError if specified CSV file is not found."""
    os.chdir(tmpdir)
    tmpdir.join(".rules2").write(TEST_RULES_CSVSTR)
    with pytest.raises(NoRulefileError):
        return_list_of_lists_pyobj_from_rules_csvfile(csvfile=".rules3")
