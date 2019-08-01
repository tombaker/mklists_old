"""Tests for todo.py

Edit /Users/tbaker/github/tombaker/mklists/mklists/backups.py
"""

import os
from mklists.backups import delete_older_backups


def test_backups_delete_older_backups(tmpdir):
    backups = ".backups"
    tmpdir_backupdir = tmpdir.mkdir(backups)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-06_0112_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-01_1230_06488910")
    shortname = "agenda"
    how_many_backups_to_keep = 2
    expected = ["2019-01-03_1646_06488910", "2019-01-06_0112_06488910"]
    print(str(expected))
    delete_older_backups(
        rootdir_pathname=tmpdir,
        backups_dirname=backups,
        backup_shortname=shortname,
        backup_depth=how_many_backups_to_keep,
    )
    assert sorted(os.listdir(tmpdir_backupdir_agenda)) == expected
