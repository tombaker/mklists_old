"""Deletes oldest backup directories, keeping only a specified (configurable) number."""

import os
import pytest
from mklists.sideeffects import delete_older_backupdirs


def test_backups_delete_older_backupdirs(tmpdir):
    """Deletes all but the latest two backup directories, as configured."""
    backupdir_subdir_name = ".backups"
    tmpdir_backupdir = tmpdir.mkdir(backupdir_subdir_name)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-06_0112_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-01_1230_06488910")
    backupdir_shortname = "agenda"
    how_many_backups_to_keep = 2
    delete_older_backupdirs(
        _rootdir_pathname=tmpdir,
        _backupdir_subdir_name=backupdir_subdir_name,
        _backupdir_shortname=backupdir_shortname,
        _backup_depth_int=how_many_backups_to_keep,
    )
    expected = ["2019-01-03_1646_06488910", "2019-01-06_0112_06488910"]
    assert sorted(os.listdir(tmpdir_backupdir_agenda)) == expected


def test_backups_delete_older_backupdirs_when_backup_depth_is_none(tmpdir):
    """Raises exception when argument for backup depth is None."""
    # TODO: 2019-08-16 Default is None, and if argument is not specified,
    #  delete_older_backupdirs() should revert to default of 2.
    backupdir_subdir_name = ".backups"
    tmpdir_backupdir = tmpdir.mkdir(backupdir_subdir_name)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    backupdir_shortname = "agenda"
    with pytest.raises(SystemExit):
        delete_older_backupdirs(
            _rootdir_pathname=tmpdir,
            _backupdir_subdir_name=backupdir_subdir_name,
            _backupdir_shortname=backupdir_shortname,
            _backup_depth_int=None,
        )


def test_backups_delete_older_backupdirs_when_backup_depth_is_zero(tmpdir):
    """Deletes all backup directories when value of backup depth argument is zero."""
    backupdir_subdir_name = ".backups"
    tmpdir_backupdir = tmpdir.mkdir(backupdir_subdir_name)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    backupdir_shortname = "agenda"
    backup_depth_int = 0
    delete_older_backupdirs(
        _rootdir_pathname=tmpdir,
        _backupdir_subdir_name=backupdir_subdir_name,
        _backupdir_shortname=backupdir_shortname,
        _backup_depth_int=backup_depth_int,
    )
    expected = []
    assert sorted(os.listdir(tmpdir_backupdir_agenda)) == expected
