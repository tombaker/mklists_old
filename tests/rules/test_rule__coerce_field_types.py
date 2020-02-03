"""Coerce strings of YAML origin to required types."""


import pytest
from mklists.ruleclass import Rule

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


@pytest.mark.skip
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
