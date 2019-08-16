"""Returns compiled regex from regular expression."""


import pytest
import re
from mklists.utils import return_compiled_regex


def test_return_compiled_regex():
    """Returns compiled regex from simple string."""
    regex = "NOW"
    assert type(return_compiled_regex(regex)) == re.Pattern


def test_return_compiled_regex_unescaped_parenthesis():
    """Raises exception when trying to compile regex with unescaped parenthesis."""
    regex = "N(OW"
    with pytest.raises(SystemExit):
        return_compiled_regex(regex)


def test_return_compiled_regex_with_escaped_parenthesis():
    """Returns compiled regex with escaped parenthesis."""
    regex = "N\(OW"
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "N(OW")


def test_return_compiled_regex_with_unescaped_backslash():
    """Raises exception when trying to compile regex with unescaped backslash."""
    regex = "N\OW"
    with pytest.raises(SystemExit):
        return_compiled_regex(regex)


def test_return_compiled_regex_with_escaped_backslash():
    """Raises exception when trying to compile regex with escaped backslash."""
    regex = "N\\OW"
    with pytest.raises(SystemExit):
        return_compiled_regex(regex)


def test_return_compiled_regex_with_double_escaped_backslash():
    """Compiles regex with double-escaped backslash."""
    regex = "N\\\\OW"
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "N\OW")


def test_return_compiled_regex_uses_backslash_sequence():
    """Returns compiled regex from string with backslash sequence."""
    regex = "\d\d\d"
    regex_compiled = return_compiled_regex(regex)
    assert type(return_compiled_regex(regex)) == re.Pattern
    assert re.search(regex_compiled, "123")


def test_return_compiled_regex_with_phone_number_regex():
    """Returns compiled regex from regex for a US telephone number."""
    regex = "^(\d{3})-(\d{3})-(\d{4})$"
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "216-321-1234")


def test_return_compiled_regex_with_blanks():
    """Returns compiled regex from regex with blank spaces."""
    regex = "^(\d{3}) (\d{3}) (\d{4})$"
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "216 321 1234")


def test_return_compiled_regex_with_uppercase_letters_only():
    """Returns compiled regex from regex with uppercase characters."""
    regex = "^[A-Z]*$"
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "ASDF")


def test_return_compiled_regex_with_wildcards_and_one_space():
    """Returns compiled regex from regex with uppercase characters."""
    regex = "^=* "
    regex_compiled = return_compiled_regex(regex)
    assert re.search(regex_compiled, "= ")
    assert re.search(regex_compiled, "== ")
    assert re.search(regex_compiled, "====== ")
