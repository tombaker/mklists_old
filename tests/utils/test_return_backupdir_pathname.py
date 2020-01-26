"""Returns full pathname of backup directory."""

import os
from pathlib import Path
from mklists.constants import TIMESTAMP_STR, BACKUPS_DIR_NAME, CONFIG_YAMLFILE_NAME
from mklists.utils import return_backup_subdir, return_backupdir_pathname


def test_return_backupdir_pathname(tmp_path):
    """Returns backup directory name from given components."""
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    backupsdir = BACKUPS_DIR_NAME
    subdir = return_backup_subdir()
    timestamp = TIMESTAMP_STR
    actual = return_backupdir_pathname(backup_subdir=subdir)
    expected = Path(tmp_path) / backupsdir / subdir / timestamp
    assert actual == expected
