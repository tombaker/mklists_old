"""Datafile contents having been captured in a Python list,
moves datafiles to backup directory.

These tests emulate return_backupdir_pathname() by
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
    move_all_datafiles_to_backupdir(datadir=tmp_datadir, backupdir=tmp_backupdir)
    expected = ["a.txt", "b.txt"]
    assert sorted(os.listdir(tmp_backupdir)) == expected
    assert sorted(os.listdir(tmp_datadir)) == []


@pytest.mark.skip
def test_move_all_datafiles_to_backupdir2(tmpdir):
    """Moves data files to backup directory."""
    backupdir_name = "_backups"
    backup_subdir_shortname = "agenda"
    timestamp_str = "2019-07-26_0758_06488910"
    backupdir_pathname = tmpdir.mkdir(
        os.path.join(backupdir_name, backup_subdir_shortname, timestamp_str)
    )
    print(f"backupdir_pathname is {backupdir_pathname}")
    assert (
        os.path.join(backupdir_name, backup_subdir_shortname, timestamp_str)
        == os.getcwd()
    )

    # print(f"backupdir_pathname is {backupdir_pathname}")
    # print(f"backupdir_pathname is {backupdir_pathname}")
    # print(f"backupdir_pathname is {backupdir_pathname}")
    # print(f"backupdir_pathname is {backupdir_pathname}")
    # print(f"backupdir_pathname is {backupdir_pathname}")
    # print(f"backupdir_pathname is {backupdir_pathname}")
    # datadir_pathname = tmpdir.mkdir(backup_subdir_shortname) # Yes, really!
    # datadir_pathname.join("file_a").write("some content")
    # datadir_pathname.join("file_b").write("some content")
    # os.chdir(datadir_pathname)
    # move_all_datafiles_to_backupdir(
    #     datadir_pathname=datadir_pathname, backupdir_pathname=backupdir_pathname
    # )
    # expected = ["file_a", "file_b"]
    # assert sorted(os.listdir(backupdir_pathname)) == expected
    # assert sorted(os.listdir(datadir_pathname)) == []


@pytest.mark.skip
def test_move_all_datafiles_to_backupdir_no_datadir_specified(tmpdir):
    """Sets default of current directory if datadir directory is specified."""
    before_cwd = os.getcwd()
    backupdir_name = "_backups"
    backup_subdir_shortname = "2020-01-24"
    datadir_pathname = tmpdir.mkdir(backup_subdir_shortname)
    datadir_pathname.join("file_a").write("some content")
    datadir_pathname.join("file_b").write("some content")
    tmpdir_backupdir = tmpdir.mkdir(backupdir_name)
    backupdir_pathname = tmpdir_backupdir.mkdir("some_directory")
    move_all_datafiles_to_backupdir(
        datadir_pathname=None, backupdir_pathname=backupdir_pathname
    )
    assert before_cwd == os.getcwd()


def test_move_all_datafiles_to_backupdir_no_backupdir_specified(tmpdir):
    """Raises exception if no backup directory is specified."""
    datadir_pathname = tmpdir.mkdir("a")
    os.chdir(datadir_pathname)
    datadir_pathname.join("file_a").write("some content")
    datadir_pathname.join("file_b").write("some content")
    with pytest.raises(SystemExit):
        move_all_datafiles_to_backupdir(datadir=datadir_pathname, backupdir=None)
