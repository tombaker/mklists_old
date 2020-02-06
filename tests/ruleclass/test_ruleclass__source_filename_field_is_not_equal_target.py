"""Some rule module tests use temporary directory fixture."""

import pytest
from mklists.ruleclass import Rule


def test_rule_source_filename_field_is_not_equal_target():
    """Source and target fields of rule object are not equivalent."""
    rule_obj = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert rule_obj._source_filename_field_is_not_equal_target


def test_rule_source_filename_field_is_not_equal_target_oops():
    """Source and target fields of rule object are same, raises SystemExit."""
    rule_obj = Rule("1", "NOW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        rule_obj._source_filename_field_is_not_equal_target()
