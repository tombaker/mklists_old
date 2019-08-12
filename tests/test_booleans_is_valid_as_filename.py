"""@@@Docstring"""

import os
import pytest
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
    r"""Note: previously assigned bad patterns as follows:
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]

    Note: in YAML, the Python string "\\.swp$" should be expressed either:
    * in quotes, with escaped backslash: '\\.swp$'
    * without quotes: \.swp$
    """
    fname = "foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert is_valid_as_filename(
        _file_tobetested_name=fname, _invalid_filename_regexes_list=bad_patterns
    )


def test_utils_is_valid_as_filename_dotfile():
    fname = ".foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        is_valid_as_filename(
            _file_tobetested_name=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )


def test_utils_is_valid_as_filename_dotfile_emacs_backup_file():
    fname = "foobar.txt~"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        is_valid_as_filename(
            _file_tobetested_name=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )


def test_utils_is_valid_as_filename_bad_filename_extension():
    fname = "foobar.swp"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        is_valid_as_filename(
            _file_tobetested_name=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )
