"""Returns shortname of directory (slashes to underscores) given rootdir pathname."""

import os
import pytest
from pathlib import Path
from mklists.utils import return_backup_subdir


def test_return_backup_subdir():
    """Returns shortname given current and root directory pathnames."""
    here = Path("/Users/tbaker/foobar/agenda")
    root = Path("/Users/tbaker/foobar")
    expected = "agenda"
    assert return_backup_subdir(work_dir=here, root_dir=root) == expected


def test_return_backup_subdir_ending_with_slash():
    """Returns shortname correctly even if working directory name ends with slash."""
    here = Path("/Users/tbaker/foobar/agenda/")
    root = Path("/Users/tbaker/foobar")
    expected = "agenda"
    assert return_backup_subdir(work_dir=here, root_dir=root) == expected


def test_return_backup_subdir_given_startdir_three_levels_deep():
    """Returns shortname when current directory is three levels deep."""
    here = Path("/Users/tbaker/foobar/a/b/c")
    root = Path("/Users/tbaker/foobar")
    expected = "a_b_c"
    assert return_backup_subdir(work_dir=here, root_dir=root) == expected


def test_return_backup_subdir_given_constants(tmp_path):
    """Returns shortname from derived start and root directory pathnames."""
    os.chdir(tmp_path)
    Path("a/b/c").mkdir(parents=True, exist_ok=True)
    os.chdir("a/b/c")
    here = Path.cwd()
    root = Path(tmp_path)
    expected = "a_b_c"
    assert return_backup_subdir(work_dir=here, root_dir=root) == expected


def test_return_backup_subdir_raise_exception_if_rootdir_is_none(tmp_path):
    """Raises exception if no rootdir is found (rootdir is None)."""
    os.chdir(tmp_path)
    with pytest.raises(SystemExit):
        return_backup_subdir()
