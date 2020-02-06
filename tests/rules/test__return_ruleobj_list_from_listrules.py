"""Return rule object list from list of lists of rule components."""

import pytest
from mklists.exceptions import NoRulesError
from mklists.ruleclass import Rule
from mklists.rules import _return_ruleobj_list_from_listrules

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


@pytest.mark.skip
@pytest.mark.rules
def test_return_ruleobj_list_from_listrules():
    """Returns list of Rule objects from Python list of five-item lists."""
    pyobj = TEST_RULES_CSVSTR_PARSED
    expected = TEST_RULEOBJ_LIST
    real = _return_ruleobj_list_from_listrules(pyobj=pyobj)
    assert real == expected


@pytest.mark.rules
def test_return_ruleobj_list_from_listrules_but_no_pyobj_as_argument():
    """Raises NoRulesError if no Python object is specified as argument."""
    with pytest.raises(NoRulesError):
        _return_ruleobj_list_from_listrules(pyobj=None)
