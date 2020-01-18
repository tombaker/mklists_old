"""@@@Docstring"""

import os
import pytest
from mklists.booleans import filename_is_valid_as_filename

# pylint: disable=bad-continuation
# Black disagrees.


def test_utils_filename_is_valid_as_filename():
    """Passes when filename is valid."""
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert filename_is_valid_as_filename("foobar.txt")


def test_utils_filename_is_valid_as_filename_exits_when_illegal_character_used():
    """Returns False when illegal semicolon encountered in filename."""
    assert filename_is_valid_as_filename("foo;bar.txt") is False


def test_utils_filename_is_valid_as_filename_exits_when_exists_as_dirname(tmpdir):
    """Exits when Docstring"""
    tmpdir.mkdir("foobar")
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        filename_is_valid_as_filename("foobar")


def test_utils_filename_is_valid_as_filename_false_because_dotfile():
    """Returns False for filename of hidden dotfile."""
    fname = ".foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            filename=fname, invalid_filename_patterns=bad_patterns
        )
        is False
    )


def test_utils_filename_is_valid_as_filename_false_because_emacs_backup_file():
    """Returns False for filename of an Emacs backup file."""
    fname = "foobar.txt~"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            filename=fname, invalid_filename_patterns=bad_patterns
        )
        is False
    )


def test_utils_filename_is_valid_as_filename_bad_filename_extension():
    """@@@Docstring"""
    fname = "foobar.swp"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            filename=fname, invalid_filename_patterns=bad_patterns
        )
        is False
    )
