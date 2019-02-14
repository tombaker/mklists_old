"""Some rule module tests use temporary directory fixture."""

import pytest
from mklists.rules import Rule


def test_rule_source_is_not_equal_target():
    """Source and target fields of rule object are not equivalent."""
    x = Rule("1", "NOW", "a.txt", "b.txt", "0")
    assert x._source_is_not_equal_target


def test_rule_source_is_not_equal_target_oops():
    """Source and target fields of rule object are same, raises SystemExit."""
    x = Rule("1", "NOW", "a.txt", "a.txt", "0")
    with pytest.raises(SystemExit):
        x._source_is_not_equal_target()
