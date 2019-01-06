"""@@@Docstring"""

from mklists.utils import return_listdir_shortname


def test_utils_return_listdir_shortname():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert return_listdir_shortname(rootdir=root_dir, listdir=list_dir) == expected


def test_utils_return_listdir_shortname_two_deep():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert return_listdir_shortname(rootdir=root_dir, listdir=list_dir) == expected
