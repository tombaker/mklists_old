"""Returns full pathname of backup directory."""

import os
import pytest
from pathlib import Path
from mklists.constants import CONFIG_YAMLFILE_NAME
from mklists.utils import return_backupdir_pathname


def test_return_backupdir_pathname(tmp_path):
    """Returns backups Path named for default working directory."""
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    backdir = "_backups"
    datestr = "2020-01-03_1646"
    workingdir = Path("agenda")
    workingdir.mkdir()
    os.chdir(workingdir)
    actual = return_backupdir_pathname(backupsdir=backdir, timestamp=datestr)
    expected = Path(tmp_path) / backdir / str(workingdir) / datestr
    expected_explicit = Path(tmp_path) / "_backups" / "agenda" / "2020-01-03_1646"
    assert actual == expected
    assert actual == expected_explicit


def test_return_backupdir_pathname_given_workdir(tmp_path):
    """Returns backups Path named for specified working directory."""
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    workingdir = Path(tmp_path).joinpath("todolists/a")
    workingdir.mkdir(parents=True, exist_ok=True)
    workingdir_shortname_expected = "todolists_a"
    backdir = "_backups"
    datestr = "2020-01-03_1646_06488910"
    actual = return_backupdir_pathname(
        workdir=workingdir, backupsdir=backdir, timestamp=datestr
    )
    expected = Path(tmp_path) / backdir / workingdir_shortname_expected / datestr
    assert actual == expected


def test_return_backupdir_pathname_given_workdir_with_slash(tmp_path):
    """Returns backups Path named for specified working directory ending with slash."""
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    workingdir = Path(tmp_path).joinpath("todolists/a/")
    workingdir.mkdir(parents=True, exist_ok=True)
    workingdir_shortname_expected = "todolists_a"
    backdir = "_backups"
    datestr = "2020-01-03_1646_06488910"
    actual = return_backupdir_pathname(
        workdir=workingdir, backupsdir=backdir, timestamp=datestr
    )
    expected = Path(tmp_path) / backdir / workingdir_shortname_expected / datestr
    assert actual == expected


def test_return_backupdir_pathname_raise_exception_if_rootdir_not_found(tmp_path):
    """Raises exception if no rootdir is found (rootdir is None)."""
    os.chdir(tmp_path)
    with pytest.raises(SystemExit):
        return_backupdir_pathname()
