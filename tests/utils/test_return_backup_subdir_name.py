"""Returns shortname of directory (slashes to underscores) given rootdir pathname."""

import os
from pathlib import Path
from mklists.utils import return_backup_subdir_name


def test_return_backup_subdir_name():
    """Returns shortname given current and root directory pathnames."""
    root = "/Users/tbaker/foobar"
    here = "/Users/tbaker/foobar/agenda"
    expected = "agenda"
    assert return_backup_subdir_name(rootdir=root, heredir=here) == expected


def test_return_backup_subdir_name_given_startdir_three_levels_deep():
    """Returns shortname when current directory is three levels deep."""
    root = "/Users/tbaker/foobar"
    here = "/Users/tbaker/foobar/a/b/c"
    expected = "a_b_c"
    assert return_backup_subdir_name(rootdir=root, heredir=here) == expected


def test_return_backup_subdir_name_given_constants(tmp_path):
    """Returns shortname from derived start and root directory pathnames."""
    os.chdir(tmp_path)
    Path("a/b/c").mkdir(parents=True, exist_ok=True)
    os.chdir("a/b/c")
    root = Path(tmp_path)
    here = Path.cwd()
    expected = "a_b_c"
    assert return_backup_subdir_name(rootdir=root, heredir=here) == expected
