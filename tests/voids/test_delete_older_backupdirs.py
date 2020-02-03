"""Delete oldest backup directories, keeping only specified number."""

import os
from pathlib import Path
from mklists.voids import delete_older_backupdirs
from mklists.constants import BACKUPS_DIR_NAME, CONFIG_YAMLFILE_NAME


def test_voids_delete_older_backupdirs_keep_two_deep(tmp_path):
    """Delete all but two subsubdirectories if backup depth is two."""
    to_keep = 2
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    Path(backups_dir).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-03").mkdir(parents=True, exist_ok=True)
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = [
        Path(backups_dir, "agenda"),
        Path(backups_dir, "agenda/2020-01-02"),
        Path(backups_dir, "agenda/2020-01-03"),
        Path(backups_dir, "agendab"),
        Path(backups_dir, "agendab/2020-01-02"),
        Path(backups_dir, "agendab/2020-01-03"),
    ]
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


def test_voids_delete_older_backupdirs_keep_all_if_backup_depth_is_greater(tmp_path):
    """Delete nothing if backup depth greater than number of subdirectories present."""
    to_keep = 7
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    Path(backups_dir).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-03").mkdir(parents=True, exist_ok=True)
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = [
        Path(backups_dir, "agenda"),
        Path(backups_dir, "agenda/2020-01-01"),
        Path(backups_dir, "agenda/2020-01-02"),
        Path(backups_dir, "agenda/2020-01-03"),
        Path(backups_dir, "agendab"),
        Path(backups_dir, "agendab/2020-01-01"),
        Path(backups_dir, "agendab/2020-01-02"),
        Path(backups_dir, "agendab/2020-01-03"),
    ]
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


def test_voids_delete_older_backupdirs_delete_all_if_backup_depth_zero(tmp_path):
    """Delete all sub-subdirectories _and_ subdirectories if backup depth is zero."""
    to_keep = 0
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    Path(backups_dir).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-03").mkdir(parents=True, exist_ok=True)
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = []
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


def test_voids_delete_older_backupdirs_delete_all_if_backup_depth_not_integer(tmp_path):
    """Delete all sub-sub- and subdirectories if backup depth not an integer."""
    to_keep = "asdf"
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    Path(backups_dir).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-03").mkdir(parents=True, exist_ok=True)
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = []
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


def test_voids_delete_older_backupdirs_delete_all_if_backup_depth_is_none(tmp_path):
    """Delete all sub-sub- and subdirectories if backup depth not an integer."""
    to_keep = None
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    Path(backups_dir).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups_dir).joinpath("agendab/2020-01-03").mkdir(parents=True, exist_ok=True)
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = []
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


def test_voids_delete_older_backupdirs_delete_nothing_if_no_backupdirs_found(tmp_path):
    """Delete nothing (obviously) if no backup directories are found."""
    to_keep = 3
    Path(tmp_path).joinpath(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    datadir = Path(tmp_path).joinpath("datadir")
    datadir.mkdir()  # create a "data directory"
    os.chdir(datadir)  # starting point would normally be a data directory
    backups_dir = Path(tmp_path).joinpath(BACKUPS_DIR_NAME)
    backups_dir.mkdir()
    delete_older_backupdirs(backups_depth=to_keep, backups_name=BACKUPS_DIR_NAME)
    expected = []
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)
