"""Return rule object list from list of lists of rule components."""

import pytest
from mklists.ruleclass import Rule
from mklists.rules import _return_ruleobj_list_from_listrules

# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.

TEST_RULES_LIST = [
    [0, ".", "x", "lines", 0],
    [1, "NOW", "lines", "alines", 1],
    [1, "LATER", "alines", "blines", 1],
    [0, "^2020", "blines", "clines", 1],
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
        source="alines",
        target="blines",
        target_sortorder=1,
    ),
    Rule(
        source_matchfield=0,
        source_matchpattern="^2020",
        source="blines",
        target="clines",
        target_sortorder=1,
    ),
]


@pytest.mark.rules
def test_return_ruleobj_list_from_listrules(reinitialize_ruleclass_variables):
    """Returns list of Rule objects from Python list of five-item lists."""
    rules_list = TEST_RULES_LIST
    expected = TEST_RULEOBJ_LIST
    real = _return_ruleobj_list_from_listrules(rules_list)
    assert real == expected


@pytest.mark.rules
def test_return_ruleobj_list_with_no_pyobj_specified(reinitialize_ruleclass_variables):
    """Raises NoRulesError if no rules list is specified as argument."""
    with pytest.raises(SystemExit):
        _return_ruleobj_list_from_listrules(pyobj=None)
