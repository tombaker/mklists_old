"""Utilities related to backups."""

import datetime
import os
import shutil
from mklists.decorators import preserve_cwd


BACKUPDIR_NAME = ".backups"
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")


def make_backup_shortname(datadir_pathname=None, rootdir_pathname=None):
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
    * for each dir in get_datadir_pathnames_under_somedir()
        accumulate a list of shortnames using make_backup_shortname(dir) => list comprehension
        accumulate a list of directory names in ".backups"
        compare the two lists and delete unused directories

    See /Users/tbaker/github/tombaker/mklists/tests/test_utils_make_backup_shortname_REDO.py
    """
    if not datadir_pathname:
        datadir_pathname = os.getcwd()
    return datadir_pathname[len(rootdir_pathname) :].strip("/").replace("/", "_")


def make_backupdir_pathname(
    reporoot_pathname=None,
    backups_dirname=None,
    backup_shortname=None,
    timestamp_name=TIMESTAMP_STR,
):
    """Generate a timestamped pathname for backups.

    Note: uses output of:
    * get_rootdir_pathname() => here: tmpdir

    Example output:

    Args:
        reporoot_pathname: Full pathname of mklists repo root directory.
        backups_dirname:
        backup_shortname:
        timestamp_name:
    """
    return os.path.join(
        reporoot_pathname, backups_dirname, backup_shortname, timestamp_name
    )


@preserve_cwd
def move_datafiles_to_backupdir(
    datadir_pathname=None, datadir_filenames=None, backupdir_pathname=None
):
    """
    Given list of visible files in data directory, move files to backupdir.

    See /Users/tbaker/github/tombaker/mklists/tests/test_backups_move_datafiles_to_backupdir_TODO.py
    """
    if not datadir_pathname:
        datadir_pathname = os.getcwd()
    os.chdir(datadir_pathname)
    try:
        for file in datadir_filenames:
            shutil.move(file, backupdir_pathname)
    except OSError:
        print("Got an exception")


@preserve_cwd
def delete_older_backups(
    reporoot_pathname=None,
    backups_dirname=None,
    backup_shortname=None,
    backup_depth=None,
):
    """Delete all but X number of backups of current working directory.

    Args:
        reporoot_pathname:
        backups_dirname:
        backup_shortname:
        backup_depth: Number of backups to keep [default: 2]

    See /Users/tbaker/github/tombaker/mklists/tests/test_backups_delete_older_backups_TODO.py
    """
    backupdir = os.path.join(reporoot_pathname, backups_dirname, backup_shortname)
    os.chdir(backupdir)
    ls_backupdir = sorted(os.listdir())
    print(ls_backupdir)
    while len(ls_backupdir) > backup_depth:
        timestamped_dir_to_delete = ls_backupdir.pop(0)
        shutil.rmtree(timestamped_dir_to_delete)
        print(f"rm {timestamped_dir_to_delete}")
