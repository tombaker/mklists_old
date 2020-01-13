"""@@@Docstring"""

import pytest
from mklists.config import _return_backupdir_shortname


def test_backups_return_backupdir_shortname():
    """@@@Docstring"""
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        _return_backupdir_shortname(
            rootdir_pathname=root_dir, datadir_pathname=list_dir
        )
        == expected
    )


def test_backups_return_backupdir_shortname_two_deep():
    """@@@Docstring"""
    root_dir = "/Users/tbaker/foobar"
    list_dir = "/Users/tbaker/foobar/a/b"
    expected = "a_b"
    assert (
        _return_backupdir_shortname(
            rootdir_pathname=root_dir, datadir_pathname=list_dir
        )
        == expected
    )
