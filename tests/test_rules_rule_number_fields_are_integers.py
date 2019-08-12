"""Some rule module tests use temporary directory fixture."""

from mklists.rules import Rule


def test_rule_number_fields_are_integers(reinitialize_ruleclass_variables):
    rule_obj = Rule("1", "N(OW", "a", "b", 2)
    assert rule_obj._number_fields_are_integers() == 1
