"""Returns shortname of directory (slashes to underscores) given rootdir pathname."""

import os
import pytest
from mklists.constants import (
    BACKUPDIR_SHORTNAME,
    ROOTDIR_PATHNAME,
    STARTDIR_PATHNAME,
    _return_backupdir_shortname,
)


def test_return_backupdir_shortname():
    """Returns shortname given current and root directory pathnames."""
    root_dir = "/Users/tbaker/foobar"
    start_dir = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        _return_backupdir_shortname(
            rootdir_pathname=root_dir, datadir_pathname=start_dir
        )
        == expected
    )


def test_return_backupdir_shortname_given_startdir_three_levels_deep():
    """Returns shortname when current directory is three levels deep."""
    root_dir = "/Users/tbaker/foobar"
    start_dir = "/Users/tbaker/foobar/a/b/c"
    expected = "a_b_c"
    assert (
        _return_backupdir_shortname(
            rootdir_pathname=root_dir, datadir_pathname=start_dir
        )
        == expected
    )


def test_return_backupdir_shortname_given_constants(tmpdir):
    """Returns shortname from derived start and root directory pathnames."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    root_dir = str(tmpdir)
    start_dir = os.getcwd()
    expected = "a_b_c"
    assert (
        _return_backupdir_shortname(
            rootdir_pathname=root_dir, datadir_pathname=start_dir
        )
        == expected
    )
