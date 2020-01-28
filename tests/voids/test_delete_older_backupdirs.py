"""Delete oldest backup directories, keeping only specified number."""

import os
import pytest
from pathlib import Path
from mklists.voids import delete_older_backupdirs


@pytest.mark.skip
def test_backups_delete_older_backupdirs_as_per_default(tmp_path):
    """Deletes all but latest three backup directories."""
    os.chdir(tmp_path)
    backupdir_agenda = Path(tmp_path).joinpath("_backups/agenda")
    backupdir_agenda.mkdir(parents=True, exist_ok=True)
    Path(tmp_path).joinpath(backupdir_agenda, "2020-01-03_1646_06488910").mkdir()
    Path(tmp_path).joinpath(backupdir_agenda, "2020-01-02_1201_06488910").mkdir()
    Path(tmp_path).joinpath(backupdir_agenda, "2020-01-06_0112_06488910").mkdir()
    Path(tmp_path).joinpath(backupdir_agenda, "2020-01-01_1230_06488910").mkdir()
    how_many_backups_to_keep = 2
    delete_older_backupdirs(
        backupdir=backupdir_agenda, backup_depth=how_many_backups_to_keep
    )
    expected = ["2020-01-03_1646_06488910", "2020-01-06_0112_06488910"]
    assert sorted(os.listdir(backupdir_agenda)) == expected


@pytest.mark.skip
def test_backups_delete_older_backupdirs_when_backup_depth_is_none(tmp_path):
    """Raises exception when argument for backup depth is None."""
    # TODO: 2019-08-16 Default is None, and if argument is not specified,
    #  delete_older_backupdirs() should revert to default of 2.
    backup_subdir_name = "_backups"
    tmpdir_backupdir = tmp_path.mkdir(backup_subdir_name)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    backupdir_shortname = "agenda"
    with pytest.raises(SystemExit):
        delete_older_backupdirs(
            backup_subdir=backup_subdir_name,
            _backupdir_shortname=backupdir_shortname,
            backup_depth=None,
        )


@pytest.mark.skip
def test_backups_delete_older_backupdirs_when_backup_depth_is_zero(tmpdir):
    """Deletes all backup directories when value of backup depth argument is zero."""
    backup_subdir_name = ".backups"
    tmpdir_backupdir = tmpdir.mkdir(backup_subdir_name)
    tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
    tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
    tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
    backupdir_shortname = "agenda"
    backup_depth_int = 0
    delete_older_backupdirs(
        rootdir=tmpdir,
        _backup_subdir_name=backup_subdir_name,
        _backupdir_shortname=backupdir_shortname,
        backup_depth=backup_depth_int,
    )
    expected = []
    assert sorted(os.listdir(tmpdir_backupdir_agenda)) == expected
