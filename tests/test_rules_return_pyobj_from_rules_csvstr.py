"""@@@Docstring"""

import io
import os
import pytest

# from mklists.constants import RULE_CSVFILE_NAME
from mklists.exceptions import NoRulesError
from mklists.rules import _return_pyobj_from_rules_csvstr

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR = "0|.|x|lines|0|A comment\n1|NOW|lines|alines|1|Another comment\n1|LATER|lines|alines|1|\n0|^2019-...|lines|blines|1|\n"

PYOBJ = [
    ["0", ".", "x", "lines", "0", "A comment"],
    ["1", "NOW", "lines", "alines", "1", "Another comment"],
    ["1", "LATER", "lines", "alines", "1", ""],
    ["0", "^2019 ..", "lines", "blines", "1", ""],
]


def test_run_return_pyobj_from_rules_csvstr(tmpdir):
    """@@@Docstring"""
    expected = PYOBJ
    real = _return_pyobj_from_rules_csvstr(csvstr=TEST_RULES_CSVSTR)
    assert real == expected


def test_run_return_pyobj_from_rules_csvstr_no_rules(tmpdir):
    """@@@Docstring"""
    with pytest.raises(NoRulesError):
        _return_pyobj_from_rules_csvstr(csvstr=None)
