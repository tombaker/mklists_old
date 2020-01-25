"""Returns full pathname of backup directory."""

import os
import pytest
from pathlib import Path
from mklists.constants import TIMESTAMP_STR, BACKUPS_DIR_NAME
from mklists.utils import (
    return_backup_subdir_name,
    return_rootdir_pathname,
    return_backupdir_pathname,
)


@pytest.mark.skip
def test_return_backupdir_pathname(tmp_path):
    """Returns backup directory name from computed components."""
    os.chdir(tmp_path)
    root = return_rootdir_pathname()
    backupdir = BACKUPS_DIR_NAME
    sub = return_backup_subdir_name()
    timestamp = TIMESTAMP_STR
    actual = return_backupdir_pathname(rootdir=root, backup_subdir=sub)
    expected = Path(root) / backupdir / sub / timestamp
    assert actual == expected


@pytest.mark.skip
def test_return_backupdir_pathname2(tmp_path):
    """Returns backup directory name from given components."""
    root = Path("/Users/tbaker/github/foo")
    bakdir = ".backups"
    sub = "agenda"
    timestamp = "20200125"
    expected = Path(root) / bakdir / sub / timestamp
    print(expected)
    actual = return_backupdir_pathname(
        rootdir=root, backupsdir=bakdir, backup_subdir=sub, timestamp=timestamp
    )
    print(actual)
    # assert actual == expected
    assert False
