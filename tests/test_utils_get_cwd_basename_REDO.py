"""@@@Docstring"""

from mklists.utils import get_cwd_basename


def test_utils_get_cwd_basename():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert get_cwd_basename(rootdir=root_dir, listdir=list_dir) == expected


def test_utils_get_cwd_basename_two_deep():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert get_cwd_basename(rootdir=root_dir, listdir=list_dir) == expected
