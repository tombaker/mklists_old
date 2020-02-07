"""Datafile contents having been captured in a Python list,
moves datafiles to backup directory.

These tests emulate get_backupdir_path() by
composing the backup directory name from the following
components:

* root directory pathname  - here: tmpdir
* backupdir_name           - here: "_backups"
* backup_subdir_shortname  - here: "agenda"
* timestamp_str            - here: "2019-07-26_0758_06488910"
"""

import os
from pathlib import Path
import pytest
from mklists.voids import move_all_datafiles_to_backupdir


def test_move_all_datafiles_to_backupdir(tmp_path):
    """Moves data files to backup directory."""
    os.chdir(tmp_path)
    tmp_backupdir = Path(tmp_path / "_backups/agenda/2019-07-26_0758_06488910")
    tmp_backupdir.mkdir(parents=True, exist_ok=True)
    tmp_datadir = Path(tmp_path / "data")
    tmp_datadir.mkdir()
    os.chdir(tmp_datadir)
    Path("a.txt").write_text("some content")
    Path("b.txt").write_text("some content")
    move_all_datafiles_to_backupdir(backupdir=tmp_backupdir, datadir=tmp_datadir)
    expected = ["a.txt", "b.txt"]
    assert sorted(os.listdir(tmp_backupdir)) == expected
    assert sorted(os.listdir(tmp_datadir)) == []


def test_move_all_datafiles_to_backupdir2(tmp_path):
    """Moves data files to backup directory."""
    os.chdir(tmp_path)
    tmp_backupdir = Path(tmp_path).joinpath("_backups/agenda/2019-07-26_0758_06488910")
    tmp_backupdir.mkdir(parents=True, exist_ok=True)
    tmp_datadir = Path(tmp_path).joinpath("data")
    tmp_datadir.mkdir()
    os.chdir(tmp_datadir)
    Path("a.txt").write_text("some content")
    Path("b.txt").write_text("some content")
    move_all_datafiles_to_backupdir(backupdir=tmp_backupdir, datadir=tmp_datadir)
    expected = ["a.txt", "b.txt"]
    assert sorted(os.listdir(tmp_backupdir)) == expected
    assert os.listdir(tmp_datadir) == []


def test_move_all_datafiles_to_backupdir_no_datadir_specified(tmp_path):
    """Sets default of current directory if datadir directory is specified."""
    os.chdir(tmp_path)
    tmp_backupdir = Path(tmp_path).joinpath("_backups/agenda/2019-07-26_0758_06488910")
    tmp_backupdir.mkdir(parents=True, exist_ok=True)
    tmp_datadir = Path(tmp_path).joinpath("data")
    tmp_datadir.mkdir()
    os.chdir(tmp_datadir)
    Path("a.txt").write_text("some content")
    move_all_datafiles_to_backupdir(backupdir=tmp_backupdir)
    assert Path(tmp_backupdir).joinpath("a.txt").is_file()


def test_move_all_datafiles_to_backupdir_no_backupdir_specified(tmp_path):
    """Raises exception if no backup directory is specified."""
    tmp_datadir = Path(tmp_path / "a")
    with pytest.raises(SystemExit):
        move_all_datafiles_to_backupdir(backupdir=None, datadir=tmp_datadir)
