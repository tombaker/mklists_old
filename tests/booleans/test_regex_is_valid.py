"""Returns True is regular expression is valid (as a regular expression)."""

from mklists.booleans import regex_is_valid


def test_regex_is_valid():
    """Returns True because regex is valid."""
    assert regex_is_valid("$NOW")


def test_regex_not_valid_unterminated_character_set():
    """Returns False because regex does not compile."""
    assert not regex_is_valid("[")
