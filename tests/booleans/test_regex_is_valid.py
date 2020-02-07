"""Returns True is regular expression is valid (as a regular expression)."""

from mklists.booleans import regex_is_valid_as_regex


def test_regex_is_valid_as_regex():
    """Returns True because regex is valid."""
    assert regex_is_valid_as_regex("$NOW")


def test_regex_is_valid_as_regex_unterminated_character_set():
    """Returns False because regex is invalid
    because character set is not terminated."""
    assert not regex_is_valid_as_regex("[")
