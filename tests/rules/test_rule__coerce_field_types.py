"""Coerce strings of YAML origin to the following types for fields:
    source_matchfield: int
    source_matchpattern: str
    source: str
    target: str
    target_sortorder: int"""

import pytest
from mklists.rules import Rule

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


def test_rule__coerce_field_types(reinitialize_ruleclass_variables):
    """Typical case: fields 1 and 5 are both integers."""
    rule_obj = Rule(1, "NOW", "a", "b", 2)
    assert rule_obj._number_fields_are_integers()


def test_rule_number_fields_are_integers_first_field_is_list(
    reinitialize_ruleclass_variables
):
    """Field 1 is a list, so TypeError is raised,
    which raises NonIntegerError, thus SystemExit."""
    rule_obj = Rule([1, 2, 3], "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._number_fields_are_integers()


@pytest.mark.skip
def test_rule_number_fields_are_integers_first_field_is_string(
    reinitialize_ruleclass_variables
):
    """Field 1 is a string, so ValueError is raised,
    which raises NonIntegerError, thus SystemExit."""
    rule_obj = Rule("One", "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._number_fields_are_integers()


@pytest.mark.skip
def test_rule_number_fields_are_integers_first_field_is_number_string(
    reinitialize_ruleclass_variables
):
    """Field 1 is a string, so ValueError is raised,
    which raises NonIntegerError, thus SystemExit."""
    rule_obj = Rule("1", "NOW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._number_fields_are_integers()
