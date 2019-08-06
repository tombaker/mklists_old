"""@@@Docstring"""

import pytest
import os
from mklists.booleans import is_valid_as_filename


def test_utils_is_valid_as_filename_exits_filename_uses_illegal_character():
    """Semicolon is illegal in filename."""
    assert is_valid_as_filename(_file_tobetested_name="foo;bar.txt") is False


def test_utils_is_valid_as_filename_exits_already_used_as_directory_name(tmpdir):
    fname = "foobar"
    tmpdir.mkdir("foobar")
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        is_valid_as_filename(_file_tobetested_name=fname)


def test_utils_is_valid_as_filename():
    fname = "foobar.txt"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert is_valid_as_filename(
        _file_tobetested_name=fname, _invalid_filename_regexes=bad_patterns
    )


def test_utils_is_valid_as_filename_dotfile():
    fname = ".foobar.txt"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert (
        is_valid_as_filename(
            _file_tobetested_name=fname, _invalid_filename_regexes=bad_patterns
        )
        is False
    )


def test_utils_is_valid_as_filename_bad_filename_extension():
    fname = "foobar.swp"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert (
        is_valid_as_filename(
            _file_tobetested_name=fname, _invalid_filename_regexes=bad_patterns
        )
        is False
    )
