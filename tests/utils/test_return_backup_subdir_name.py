"""Returns shortname of directory (slashes to underscores) given rootdir pathname."""

import os
from mklists.utils import return_backup_subdir_name


def test_return_backup_subdir_name():
    """Returns shortname given current and root directory pathnames."""
    root_dir = "/Users/tbaker/foobar"
    startdir_pathname = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert (
        return_backup_subdir_name(
            rootdir_pathname=root_dir, datadir_pathname=startdir_pathname
        )
        == expected
    )


def test_return_backup_subdir_name_given_startdir_three_levels_deep():
    """Returns shortname when current directory is three levels deep."""
    root_dir = "/Users/tbaker/foobar"
    startdir_pathname = "/Users/tbaker/foobar/a/b/c"
    expected = "a_b_c"
    assert (
        return_backup_subdir_name(
            rootdir_pathname=root_dir, datadir_pathname=startdir_pathname
        )
        == expected
    )


def test_return_backup_subdir_name_given_constants(tmpdir):
    """Returns shortname from derived start and root directory pathnames."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    root_dir = str(tmpdir)
    startdir_pathname = os.getcwd()
    expected = "a_b_c"
    assert (
        return_backup_subdir_name(
            rootdir_pathname=root_dir, datadir_pathname=startdir_pathname
        )
        == expected
    )
