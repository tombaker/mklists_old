"""Returns True if fields 1 and 5 of a rule are both integers."""

import pytest
from mklists.rules import Rule


def test_rule_number_fields_are_integers(reinitialize_ruleclass_variables):
    """Fields 1 and 5 are both integers."""
    rule_obj = Rule(1, "N(OW", "a", "b", 2)
    assert rule_obj._number_fields_are_integers()


def test_rule_number_fields_are_integers_or_can_be_converted(
    reinitialize_ruleclass_variables
):
    """Field 1 is already integer; field 5 is an integer after conversion."""
    rule_obj = Rule(1, "N(OW", "a", "b", "2")
    assert rule_obj._number_fields_are_integers()


def test_rule_number_fields_are_integers_first_field_is_string(
    reinitialize_ruleclass_variables
):
    """Field 1 is a string, so ValueError is raised,
    which raises NonIntegerError, thus SystemExit."""
    rule_obj = Rule("One", "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._number_fields_are_integers()


def test_rule_number_fields_are_integers_first_field_is_list(
    reinitialize_ruleclass_variables
):
    """Field 1 is a list, so TypeError is raised,
    which raises NonIntegerError, thus SystemExit."""
    rule_obj = Rule([1, 2, 3], "N(OW", "a", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._number_fields_are_integers()
