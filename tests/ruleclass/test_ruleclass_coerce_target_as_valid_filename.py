"""Confirm filename is valid as per filename rules."""


import pytest
from mklists.ruleclass import Rule

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


def test_target_is_valid_filename():
    """Field 4 (target) must be a valid filename."""
    rule_obj = Rule(1, "NOW", "a", "b", 2)
    rule_obj._target_is_valid_filename()
    assert isinstance(rule_obj.target, str)
    assert rule_obj.target == "b"


def test_target_is_valid_filename_raise_exception_given_bad_string():
    """Field 4 (target) must not contain invalid characters."""
    rule_obj = Rule(1, "NOW", "a", "b/2:", 2)
    with pytest.raises(SystemExit):
        rule_obj._target_is_valid_filename()


def test_target_is_valid_filename_raise_exception_given_none():
    """Field 4 (target) must not be None."""
    rule_obj = Rule(1, "NOW", "a", None, 2)
    with pytest.raises(SystemExit):
        rule_obj._target_is_valid_filename()
