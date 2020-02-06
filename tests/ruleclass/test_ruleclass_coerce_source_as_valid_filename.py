"""Coerce strings of YAML origin to required types."""


import os
import pytest
from mklists.ruleclass import Rule
from mklists.exceptions import MissingValueError

# pylint: disable=bad-continuation
# Black disagrees.
# pylint: disable=unused-argument
# In tests, fixture arguments may look like they are unused.


def test_source_is_valid_filename(tmp_path):
    """Field 3 (source) must be a valid filename."""
    os.chdir(tmp_path)
    rule_obj = Rule(1, "NOW", "a", "b", 2)
    rule_obj._source_is_valid_filename()
    assert isinstance(rule_obj.source, str)
    assert rule_obj.source == "a"


def test_source_is_valid_filename_raise_exception_given_bad_string():
    """Field 3 (source) must not contain invalid characters."""
    rule_obj = Rule(1, "NOW", "a/2:", "b", 2)
    with pytest.raises(SystemExit):
        rule_obj._source_is_valid_filename()


def test_source_is_valid_filename_raise_exception_given_none():
    """Field 3 (source) must not be None."""
    rule_obj = Rule(1, "NOW", None, "b", 2)
    with pytest.raises(MissingValueError):
        rule_obj._source_is_valid_filename()
