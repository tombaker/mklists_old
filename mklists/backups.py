"""Utilities related to backups."""

import os
import shutil
import pytest
from .constants import TIMESTAMP_STR
from .decorators import preserve_cwd


@preserve_cwd
def delete_older_backups(
    _rootdir_pathname=None,
    _backupdir_subdir_name=None,
    _backupdir_shortname=None,
    _backup_depth_int=None,
):
    """Delete all but X number of backups of current working directory.

    Args:
        _rootdir_pathname:
        _backupdir_subdir_name:
        _backupdir_shortname:
        _backup_depth_int: Number of backups to keep [default: 2]

    See /Users/tbaker/github/tombaker/mklists/tests/test_backups_delete_older_backups_TODO.py
    """
    backupdir = os.path.join(
        _rootdir_pathname, _backupdir_subdir_name, _backupdir_shortname
    )
    os.chdir(backupdir)
    ls_backupdir = sorted(os.listdir())
    print(ls_backupdir)
    while len(ls_backupdir) > _backup_depth_int:
        timestamped_dir_to_delete = ls_backupdir.pop(0)
        shutil.rmtree(timestamped_dir_to_delete)
        print(f"rm {timestamped_dir_to_delete}")


@pytest.mark.improve
@preserve_cwd
def move_datafiles_to_backupdir(
    _datadir_pathname=None, _datafiles_names=None, _backupdir_pathname=None
):
    """Move data files to backup directory.

    "Data files" are all visible files in the data directory.

    Args:
        _datadir_pathname: Pathname of the data directory,
          (typically? always?) the current working directory.
        _datafiles_names: Names of all visible files in the data
          directory (pre-checked to ensure they are text files?).
        _backupdir_pathname: Pathname of the backup directory.
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    os.chdir(_datadir_pathname)
    try:
        for file in _datafiles_names:
            shutil.move(file, _backupdir_pathname)
    except OSError:
        print("Got an exception")


def return_backupdir_pathname(
    _rootdir_pathname=None,
    _backupdir_subdir_name=None,
    _backupdir_shortname=None,
    _timestamp_str=TIMESTAMP_STR,
):
    """Generate a timestamped pathname for backups.

    Note: uses output of:
    * return_rootdir_pathname() => here: tmpdir

    Example output:

    Args:
        _rootdir_pathname: Full pathname of mklists repo root directory.
        _backupdir_subdir_name:
        _backupdir_shortname:
        _timestamp_str:
    """
    return os.path.join(
        _rootdir_pathname, _backupdir_subdir_name, _backupdir_shortname, _timestamp_str
    )


def return_backupdir_shortname(_datadir_pathname=None, _rootdir_pathname=None):
    """Creates shortname for backup directory:
    * if directory is on top level, shortname is same as directory name
    * if directory is nested, shortname is chain of directory names separated by underscores

    Note: test for edge case where the following three subdirectories exist:
        .
        ├── a
        │   └── b
        └── a_b

    Problem: "a_b" and "a/b" would both translate into shortname of "a_b" (clash)
    Solutions?
    * Use two underscores instead of one?
    * for each dir in return_datadir_pathnames_under_somedir()
        accumulate a list of shortnames using return_backupdir_shortname(dir) => list comprehension
        accumulate a list of directory names in ".backups"
        compare the two lists and delete unused directories

    See /Users/tbaker/github/tombaker/mklists/tests/test_utils_return_backupdir_shortname_REDO.py
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    return _datadir_pathname[len(_rootdir_pathname) :].strip("/").replace("/", "_")
