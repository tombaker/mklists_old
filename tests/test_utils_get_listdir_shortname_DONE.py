"""@@@Docstring"""

from mklists.utils import get_listdir_shortname


def test_utils_get_listdir_shortname():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        get_listdir_shortname(rootdir_pathname=root_dir, listdir_pathname=list_dir)
        == expected
    )


def test_utils_get_listdir_shortname_two_deep():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert (
        get_listdir_shortname(rootdir_pathname=root_dir, listdir_pathname=list_dir)
        == expected
    )
