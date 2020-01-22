"""@@@Docstring"""

import pytest

# from mklists.constants import RULE_CSVFILE_NAME
from mklists.exceptions import NoRulesError
from mklists.rules import Rule, _return_ruleobj_list_from_pyobj

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_CSVSTR_PARSED = [
    [0, ".", "x", "lines", 0],
    [1, "NOW", "lines", "alines", 1],
    [1, "LATER", "lines", "alines", 1],
    [0, "^2020", "lines", "blines", 1],
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
        source_matchpattern="^2020",
        source="lines",
        target="blines",
        target_sortorder=1,
    ),
]


def test_return_ruleobj_list_from_pyobj():
    """Returns list of Rule objects from Python list of five-item lists."""
    pyobj = TEST_RULES_CSVSTR_PARSED
    expected = TEST_RULEOBJ_LIST
    real = _return_ruleobj_list_from_pyobj(pyobj=pyobj)
    assert real == expected


def test_return_ruleobj_list_from_pyobj_but_no_pyobj_as_argument():
    """Raises NoRulesError if no Python object is specified as argument."""
    with pytest.raises(NoRulesError):
        _return_ruleobj_list_from_pyobj(pyobj=None)


@pytest.mark.skip
def test_return_ruleobj_list_from_pyobj_but_input_pyobj_is_bad():
    """Raises some exception if Python object does not match expectations.

    Or can we expect that the input to this function will be good?"""
    TEST_RULES_CSVSTR_PARSED_BINKY = [
        [0, ".", "x", "lines", 0],
        [1, "NOW", "lines", "alines", 1],
        [1, "LATER", "lines", "alines", 1],
        [0, "^2020", "lines", "blines", "binky"],
    ]
    with pytest.raises(ValueError):
        _return_ruleobj_list_from_pyobj(pyobj=TEST_RULES_CSVSTR_PARSED_BINKY)
