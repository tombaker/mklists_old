"""Delete oldest backup directories, keeping only specified number."""

import os
import pytest
from pathlib import Path
from mklists.voids import delete_older_backupdirs
from mklists.constants import BACKUPS_DIR_NAME, CONFIG_YAMLFILE_NAME


@pytest.fixture(name="tmp_backupdir")
def fixture_backupdir_with_directories(tmp_path):
    """Return temporary mklists backup directory with subdirectories."""
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    backups = Path.cwd().joinpath("_backups")
    backups.mkdir()
    Path(backups).joinpath("agenda/2020-01-01").mkdir(parents=True, exist_ok=True)
    Path(backups).joinpath("agenda/2020-01-02").mkdir(parents=True, exist_ok=True)
    Path(backups).joinpath("agenda/2020-01-03").mkdir(parents=True, exist_ok=True)
    assert sorted(list([pth for pth in Path(backups).rglob("*")])) == sorted(
        [
            Path(backups).joinpath("agenda"),
            Path(backups).joinpath("agenda/2020-01-01"),
            Path(backups).joinpath("agenda/2020-01-02"),
            Path(backups).joinpath("agenda/2020-01-03"),
        ]
    )
    return backups


def test_backupdir_fixture_itself(tmp_backupdir):
    subsubdirs = []
    for subdir in Path(tmp_backupdir).glob("*"):
        for subsubdir in Path(subdir).glob("*"):
            subsubdirs.append(subsubdir)
    assert sorted(subsubdirs) == sorted(
        [
            Path(tmp_backupdir).joinpath("agenda/2020-01-01"),
            Path(tmp_backupdir).joinpath("agenda/2020-01-02"),
            Path(tmp_backupdir).joinpath("agenda/2020-01-03"),
        ]
    )


@pytest.mark.skip
def test_backups_delete_older_backupdirs_dryrun(tmp_backupdir):
    # backups_dir = BACKUPS_DIR_NAME
    print()
    print(tmp_backupdir)
    print(delete_older_backupdirs(backups_dir=BACKUPS_DIR_NAME, dryrun=True))
    assert False


def test_backups_delete_older_backupdirs_delete_extra_directories(tmp_backupdir):
    subsubdirs = []
    for subdir in Path(tmp_backupdir).glob("*"):
        for subsubdir in Path(subdir).glob("*"):
            subsubdirs.append(subsubdir)
    backups_to_keep = 2
    subsubdirs_to_delete = sorted(subsubdirs)[:-(backups_to_keep)]
    assert subsubdirs_to_delete == [Path(tmp_backupdir).joinpath("agenda/2020-01-01")]
    # import shutil
    # for subsubdir in subsubdirs_to_delete:
    #     print(f"rm -r {subsubdir}")
    #     shutil.rmtree(subsubdir)
    # assert sorted(list([pth for pth in Path(backups).rglob('*')])) == sorted([
    #     Path(backups).joinpath("agenda"),
    #     Path(backups).joinpath("agenda/2020-01-03"),
    # ])


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
