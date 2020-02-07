"""@@@Docstring"""

import os
import pathlib
import pytest
from mklists.booleans import filename_is_valid
from mklists.exceptions import FilenameIsAlreadyDirnameError, MissingValueError

# pylint: disable=bad-continuation
# Black disagrees.


def test_filename_is_valid():
    """Passes when filename is valid."""
    assert filename_is_valid("foobar.txt")


def test_filename_is_valid_exits_when_illegal_character_used():
    """Returns False when illegal semicolon encountered in filename."""
    assert filename_is_valid("foo;bar.txt") is False


def test_filename_is_invalid_if_filename_is_none(tmp_path):
    """Raises exception when given filename is None."""
    with pytest.raises(MissingValueError):
        filename_is_valid(filename=None)


def test_filename_is_valid_exits_when_exists_as_dirname(tmp_path):
    """Raises exception when given filename already exists as directory name."""
    os.chdir(tmp_path)
    name_to_be_tested = "foobar"
    foobar = pathlib.Path(name_to_be_tested)
    foobar.mkdir()
    with pytest.raises(FilenameIsAlreadyDirnameError):
        filename_is_valid(name_to_be_tested)


def test_filename_is_valid_false_because_dotfile():
    """Returns False for filename of hidden dotfile."""
    fname = ".foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid(filename=fname, invalid_filename_patterns=bad_patterns)
        is False
    )


def test_filename_is_valid_false_because_emacs_backup_file():
    """Returns False for filename of an Emacs backup file."""
    fname = "foobar.txt~"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid(filename=fname, invalid_filename_patterns=bad_patterns)
        is False
    )


def test_filename_is_valid_bad_filename_extension():
    """@@@Docstring"""
    fname = "foobar.swp"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid(filename=fname, invalid_filename_patterns=bad_patterns)
        is False
    )
