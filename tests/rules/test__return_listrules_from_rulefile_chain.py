"""Returns Python list of five-item lists from a rule file."""
# TODO 2020-01-30: uses ROOTDIR_RULEFILE_NAME now, not just DATADIR_RULEFILE_NAME

import os
import pytest
from pathlib import Path

from mklists.constants import ROOTDIR_RULEFILE_NAME
from mklists.exceptions import NoRulefileError
from mklists.rules import _return_listrules_from_rulefile_chain

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


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain(tmp_path):
    """Return True if CSV file has no header line because it will be ignored anyway."""
    os.chdir(tmp_path)
    Path(ROOTDIR_RULEFILE_NAME).write_text(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = _return_listrules_from_rulefile_chain(csvfile=ROOTDIR_RULEFILE_NAME)
    assert real == expected


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_header_ignored(tmp_path):
    """The CSV file may have a header line, though it will be ignored."""
    os.chdir(tmp_path)
    Path(ROOTDIR_RULEFILE_NAME).write_text(TEST_RULES_CSVSTR)
    expected = PYOBJ
    real = _return_listrules_from_rulefile_chain(csvfile=ROOTDIR_RULEFILE_NAME)
    assert real == expected


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_rn(tmp_path):
    """Fine for CSV file to have MS-Windows line endings (\r\n)."""
    os.chdir(tmp_path)
    Path(ROOTDIR_RULEFILE_NAME).write_text(TEST_RULES_CSVSTR_RN)
    expected = PYOBJ
    real = _return_listrules_from_rulefile_chain(csvfile=ROOTDIR_RULEFILE_NAME)
    assert real == expected


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_legacy(tmp_path):
    """Fine for CSV line to pad fields with spaces and leave field 5 blank."""
    os.chdir(tmp_path)
    Path(ROOTDIR_RULEFILE_NAME).write_text(TEST_RULES_CSVSTR_LEGACY)
    expected = PYOBJ_LEGACY
    real = _return_listrules_from_rulefile_chain(csvfile=ROOTDIR_RULEFILE_NAME)
    assert real == expected


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_rulefile_not_specified(tmp_path):
    """Raises NoRulefileError if specified CSV file is "None" (the default)."""
    with pytest.raises(NoRulefileError):
        _return_listrules_from_rulefile_chain(csvfile=None)


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_rulefile_not_specified2(tmp_path):
    """Raises NoRulefileError if called specifying no argument at all."""
    with pytest.raises(NoRulefileError):
        _return_listrules_from_rulefile_chain()


@pytest.mark.rules
def test_return_listrules_from_rulefile_chain_not_found(tmp_path):
    """Raises NoRulefileError if specified CSV file is not found."""
    os.chdir(tmp_path)
    Path(".rules2").write_text(TEST_RULES_CSVSTR)
    with pytest.raises(NoRulefileError):
        _return_listrules_from_rulefile_chain(csvfile=".rules3")
