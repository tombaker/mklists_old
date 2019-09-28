"""Returns True is regular expression is valid (as a regular expression)."""

import pytest
from mklists.booleans import regex_is_valid_as_regex


def test_regex_is_valid_as_regex():
    """Returns True because regex is valid."""
    assert regex_is_valid_as_regex("$NOW")
