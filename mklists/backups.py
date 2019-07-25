"""Utilities related to backups.

Creates directories such as the following:
    /.backups/a/2019-07-22_0907_07165222/
    /.backups/a/2019-07-23_1611_05165896/
    /.backups/a_a1/2019-07-22_0907_07165222/
    /.backups/a_a1/2019-07-23_1611_05165896/
    /.backups/logs/2019-07-22_0907_07165222/
    /.backups/logs/2019-07-23_1611_05165896/

try:
    os.remove(myfile)
except OSError as e:  ## if failed, report it back to the user ##
    print ("Error: %s - %s." % (e.filename, e.strerror))

directory_list = [ '2018-12-31_0904_23414123', '2019-01-01_1105_12155264', '2019-02-02_1831_02265324' ]

get_rootdir_pathname() / BACKUPDIR_NAME / make_backup_shortname() / TIMESTAMP_STR
"""

import datetime
import os
import shutil
from mklists.utils import preserve_cwd


BACKUPDIR_NAME = ".backups"
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")


def make_backup_shortname(datadir_pathname=None, rootdir_pathname=None):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_utils_make_backup_shortname_REDO.py
    @@@Redo this using os.path.basename"""
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

    Args:
        reporoot_pathname: Full pathname of mklists repo root directory.
        backups_dirname:
        backup_shortname:
        timestamp_name:
    """
    return os.path.join(
        reporoot_pathname, backups_dirname, backup_shortname, timestamp_name
    )


def move_datafiles_to_backupdir(backupdir, backups=2):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_datafiles_to_backupdir
    Get number of backups as configuring (config['backups']
        If backups less than two, then backups = 2 ("mandatory")
    Create a backup directory.
        Generate a name for backupdir (make_backupdir_pathname).
        Make dir: hard-coded parent dirname (_html) plus generated timestamped name.
    Get list of existing visible files in data directory.
    Move all visible files in data directory to backupdir.
        for file in filelist:
            shutil.move(file, backupdir)
    """


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
