"""@@@Docstring"""

from mklists.backups import return_backupdir_shortname


def test_backups_return_backupdir_shortname():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        return_backupdir_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
        == expected
    )


def test_backups_return_backupdir_shortname_two_deep():
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert (
        return_backupdir_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
        == expected
    )
