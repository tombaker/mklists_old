"""@@@Docstring"""

import os
import pytest
from mklists.booleans import filename_is_valid_as_filename


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename_exits_filename_uses_illegal_character():
    """Semicolon is illegal in filename."""
    assert filename_is_valid_as_filename(_filename="foo;bar.txt") is False


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename_exits_already_used_as_directory_name(
    tmpdir
):
    """@@@Docstring"""
    fname = "foobar"
    tmpdir.mkdir("foobar")
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        filename_is_valid_as_filename(_filename=fname)


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename():
    r"""Note: previously assigned bad patterns as follows:
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]

    Note: in YAML, the Python string "\\.swp$" should be expressed either:
    * in quotes, with escaped backslash: '\\.swp$'
    * without quotes: \.swp$
    """
    fname = "foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert filename_is_valid_as_filename(
        _filename=fname, _invalid_filename_regexes_list=bad_patterns
    )


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename_dotfile():
    """@@@Docstring"""
    fname = ".foobar.txt"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            _filename=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename_dotfile_emacs_backup_file():
    """@@@Docstring"""
    fname = "foobar.txt~"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            _filename=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )


@pytest.mark.skip
def test_utils_filename_is_valid_as_filename_bad_filename_extension():
    """@@@Docstring"""
    fname = "foobar.swp"
    bad_patterns = ["\\.swp$", "\\.tmp$", "~$", "^\\."]
    assert (
        filename_is_valid_as_filename(
            _filename=fname, _invalid_filename_regexes_list=bad_patterns
        )
        is False
    )
