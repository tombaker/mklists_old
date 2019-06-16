"""@@@Docstring"""

from mklists.utils import has_valid_name


def test_utils_has_valid_name():
    fname = "foobar.txt"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert has_valid_name(fname, bad_patterns)


def test_utils_has_valid_name_dotfile():
    fname = ".foobar.txt"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert has_valid_name(fname, badpats=bad_patterns) is False


def test_utils_has_valid_name_bad_filename_extension():
    fname = "foobar.swp"
    bad_patterns = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    assert has_valid_name(fname, bad_patterns) is False
