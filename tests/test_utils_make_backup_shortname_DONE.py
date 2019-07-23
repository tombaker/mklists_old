"""@@@Docstring"""

from mklists.utils import make_backup_shortname


def test_utils_make_backup_shortname():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        make_backup_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
        == expected
    )


def test_utils_make_backup_shortname_two_deep():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert (
        make_backup_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
        == expected
    )
