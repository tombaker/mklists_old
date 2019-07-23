"""Utilities related to backups.

When run, these directories would be created:
    /.backups/a/2019-07-22_0907_07165222/
    /.backups/a/2019-07-23_1611_05165896/
    /.backups/a_a1/2019-07-22_0907_07165222/
    /.backups/a_a1/2019-07-23_1611_05165896/
    /.backups/logs/2019-07-22_0907_07165222/
    /.backups/logs/2019-07-23_1611_05165896/

directory_list = [ '2018-12-31.23414123', '2019-01-01.12155264', '2019-02-02.02265324' ]

    BACKUPDIR_NAME / make_backup_shortname() / TIMESTAMP_STR
"""

import datetime
import os

BACKUPDIR_NAME = ".backups"
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")


def make_backup_shortname(datadir_pathname=None, rootdir_pathname=None):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_utils_make_backup_shortname_REDO.py
    @@@Redo this using os.path.basename"""
    if not datadir_pathname:
        datadir_pathname = os.getcwd()
    return datadir_pathname[len(rootdir_pathname) :].strip("/").replace("/", "_")


def make_backupdir_pathname(now=TIMESTAMP_STR, backupdir_name=None):
    """@@@Docstring"""
    return os.path.join(backupdir_name, now)


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


def delete_older_backups():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_delete_older_backups.py
    Count number of backups under this directory:
        Get short name of current data directory (make_backup_shortname).
        Create list of directories under parent directory of backupdir.
            lsd_visible = [item for item in glob.glob('*') if os.path.isdir(item)]
            Example: if backup dir is
                mkrepo/_backups/a/2018-12-31.23414123
            Then parent is
                mkrepo/_backups/a
            Resulting list might be:
                [ '2018-12-31.23414123', '2019-01-01.12155264', '2019-02-02.02265324' ]
    Either:
        while len(lsd_visible) > backups:
            file_to_be_deleted = lsd_visible.pop(0)
            rm file_to_be_deleted
    Or:
        while len(directory_list) > backups:
            dir_to_delete = directory_list.pop(0)
            print(f"rm {dir_to_delete}")
    """
