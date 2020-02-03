"""Delete oldest backup directories, keeping only specified number."""

import os
import pytest
from pathlib import Path
from mklists.voids import delete_older_backupdirs
from mklists.constants import BACKUPS_DIR_NAME, CONFIG_YAMLFILE_NAME


def test_voids_delete_older_backupdirs_keep_zero(tmp_path):
    """Delete all sub-subdirectories, and subdirectories, if backup depth is zero."""
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
    delete_older_backupdirs(backups_depth=0, backups_name=BACKUPS_DIR_NAME)
    expected = []
    actual = list(Path(backups_dir).rglob("*"))
    assert sorted(expected) == sorted(actual)


@pytest.mark.skip
def test_voids_delete_older_backupdirs_keep_seven(tmp_path):
    """Delete some sub-subdirectories of backups directory if backup depth is two."""
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
    delete_older_backupdirs(backups_depth=7, backups_name=BACKUPS_DIR_NAME)
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


@pytest.mark.skip
def test_voids_delete_older_backupdirs_keep_two_deep(tmp_repo_with_backupdir):
    """@@@Docstring"""
    backupsdir = Path(tmp_repo_with_backupdir).joinpath(BACKUPS_DIR_NAME)
    backups_to_keep = 2
    delete_older_backupdirs(backups_depth=backups_to_keep)  # noqa: F841
    expected = sorted(
        [
            Path(backupsdir, "agenda"),
            Path(backupsdir, "agenda/2020-01-02"),
            Path(backupsdir, "agenda/2020-01-03"),
            Path(backupsdir, "agendab"),
            Path(backupsdir, "agendab/2020-01-02"),
            Path(backupsdir, "agendab/2020-01-03"),
        ]
    )
    actual = sorted([dir for dir in Path(backupsdir).rglob("*") if dir.is_dir()])
    assert expected == actual


@pytest.mark.skip
def test_voids_delete_older_backupdirs_keep_one_deep(tmp_repo_with_backupdir):
    backupsdir = Path(tmp_repo_with_backupdir).joinpath(BACKUPS_DIR_NAME)
    backupsdir_before = sorted(
        [dir for dir in Path(backupsdir).rglob("*") if dir.is_dir()]
    )
    assert backupsdir_before == sorted(
        [
            Path(backupsdir, "agenda"),
            Path(backupsdir, "agenda/2020-01-01"),
            Path(backupsdir, "agenda/2020-01-02"),
            Path(backupsdir, "agenda/2020-01-03"),
            Path(backupsdir, "agendab"),
            Path(backupsdir, "agendab/2020-01-01"),
            Path(backupsdir, "agendab/2020-01-02"),
            Path(backupsdir, "agendab/2020-01-03"),
        ]
    )
    backups_to_keep = 1
    delete_older_backupdirs(backups_depth=backups_to_keep)  # noqa: F841
    expected = sorted(
        [
            Path(backupsdir, "agenda"),
            Path(backupsdir, "agenda/2020-01-03"),
            Path(backupsdir, "agendab"),
            Path(backupsdir, "agendab/2020-01-03"),
        ]
    )
    actual = sorted([dir for dir in Path(backupsdir).rglob("*") if dir.is_dir()])
    assert expected == actual


@pytest.mark.skip
def test_voids_delete_older_backupdirs_keep_zero_deep(tmp_repo_with_backupdir):
    backupsdir = Path(tmp_repo_with_backupdir).joinpath(BACKUPS_DIR_NAME)
    backupsdir_before = sorted(
        [dir for dir in Path(backupsdir).rglob("*") if dir.is_dir()]
    )
    assert backupsdir_before == sorted(
        [
            Path(backupsdir, "agenda"),
            Path(backupsdir, "agenda/2020-01-01"),
            Path(backupsdir, "agenda/2020-01-02"),
            Path(backupsdir, "agenda/2020-01-03"),
            Path(backupsdir, "agendab"),
            Path(backupsdir, "agendab/2020-01-01"),
            Path(backupsdir, "agendab/2020-01-02"),
            Path(backupsdir, "agendab/2020-01-03"),
        ]
    )
    backups_to_keep = 0
    delete_older_backupdirs(backups_depth=backups_to_keep)  # noqa: F841
    expected = sorted([Path(backupsdir, "agenda"), Path(backupsdir, "agendab")])
    actual = sorted([dir for dir in Path(backupsdir).rglob("*") if dir.is_dir()])
    assert expected == actual


@pytest.mark.skip
def test_voids_delete_older_backupdirs_delete_extra_directories(
    tmp_repo_with_backupdir
):
    subsubdirs = []
    for subdir in Path(tmp_repo_with_backupdir).glob("*"):
        for subsubdir in Path(subdir).glob("*"):
            subsubdirs.append(subsubdir)
    backups_to_keep = 2
    subsubdirs_to_delete = sorted(subsubdirs)[:-(backups_to_keep)]
    assert subsubdirs_to_delete == [
        Path(tmp_repo_with_backupdir).joinpath("agenda/2020-01-01")
    ]


# @pytest.mark.skip
# def test_backups_delete_older_backupdirs_when_backup_depth_is_none(tmp_path):
#     """Raises exception when argument for backup depth is None."""
#     # TODO: 2019-08-16 Default is None, and if argument is not specified,
#     #  delete_older_backupdirs() should revert to default of 2.
#     backup_subdir_name = "_backups"
#     tmpdir_backupdir = tmp_path.mkdir(backup_subdir_name)
#     tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
#     tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
#     tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
#     backupdir_shortname = "agenda"
#     with pytest.raises(SystemExit):
#         delete_older_backupdirs()
#
#
# @pytest.mark.skip
# def test_backups_delete_older_backupdirs_when_backup_depth_is_zero(tmpdir):
#     """Deletes all backup directories when value of backup depth argument is zero."""
#     backup_subdir_name = ".backups"
#     tmpdir_backupdir = tmpdir.mkdir(backup_subdir_name)
#     tmpdir_backupdir_agenda = tmpdir_backupdir.mkdir("agenda")
#     tmpdir_backupdir_agenda.mkdir("2019-01-03_1646_06488910")
#     tmpdir_backupdir_agenda.mkdir("2019-01-02_1201_06488910")
#     backupdir_shortname = "agenda"
#     backup_depth_int = 0
#     delete_older_backupdirs()
#     expected = []
#     assert sorted(os.listdir(tmpdir_backupdir_agenda)) == expected


@pytest.mark.skip
def test_backups_delete_older_backupdirs_setup_basics(tmp_path):
    """Deletes all but latest three backup directories."""
    backups = Path(tmp_path).joinpath("_backups")
    backups.mkdir()
    Path(backups).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    Path(backups).joinpath("agenda/2020-01-06").mkdir(parents=True, exist_ok=True)
    assert sorted(list([pth for pth in Path(backups).rglob("*")])) == sorted(
        [
            Path(backups).joinpath("agenda"),
            Path(backups).joinpath("agenda/2020-01-01"),
            Path(backups).joinpath("agenda/2020-01-02"),
            Path(backups).joinpath("agenda/2020-01-03"),
            Path(backups).joinpath("agenda/2020-01-06"),
        ]
    )
    subsubdirs = []
    for subdir in Path(backups).glob("*"):
        for subsubdir in Path(subdir).glob("*"):
            subsubdirs.append(subsubdir)
    assert sorted(subsubdirs) == sorted(
        [
            Path(backups).joinpath("agenda/2020-01-01"),
            Path(backups).joinpath("agenda/2020-01-02"),
            Path(backups).joinpath("agenda/2020-01-03"),
            Path(backups).joinpath("agenda/2020-01-06"),
        ]
    )
    backups_to_keep = 2
    subsubdirs_to_delete = sorted(subsubdirs)[:-(backups_to_keep)]
    assert subsubdirs_to_delete == [
        Path(backups).joinpath("agenda/2020-01-01"),
        Path(backups).joinpath("agenda/2020-01-02"),
    ]
    import shutil

    for subsubdir in subsubdirs_to_delete:
        shutil.rmtree(subsubdir)

    assert sorted(list([pth for pth in Path(backups).rglob("*")])) == sorted(
        [
            Path(backups).joinpath("agenda"),
            Path(backups).joinpath("agenda/2020-01-03"),
            Path(backups).joinpath("agenda/2020-01-06"),
        ]
    )
