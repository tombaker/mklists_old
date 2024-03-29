"""Returns root pathname of mklists repo wherever called in repo."""

import os
import pytest
from pathlib import Path
from mklists.constants import CONFIGFILE_NAME, ROOTDIR_RULEFILE_NAME
from mklists.returns import get_rootdir_path

# pylint: disable=unused-argument
# These are just tests...


def test_get_rootdir_path_while_in_rootdir_using_tmp_path(tmp_path):
    """Returns root directory when called while already in root directory."""
    os.chdir(tmp_path)
    Path(CONFIGFILE_NAME).write_text("config stuff")
    assert Path(CONFIGFILE_NAME).exists()
    assert get_rootdir_path() == tmp_path


def test_get_rootdir_path_while_in_rootdir_using_fixture(myrepo):
    """Returns root directory when called in root directory of "myrepo"."""
    os.chdir(myrepo)
    assert Path(CONFIGFILE_NAME).exists()  # created by fixture "myrepo"
    assert Path(ROOTDIR_RULEFILE_NAME).exists()  # created by fixture "myrepo"
    assert get_rootdir_path() == myrepo


def test_get_rootdir_path_from_fixture_subdir(myrepo):
    """Returns root pathname when called in subdirectory of "myrepo"."""
    os.chdir(myrepo)
    assert Path(CONFIGFILE_NAME).exists()  # created by fixture "myrepo"
    os.chdir(os.path.join(myrepo, "a"))
    assert get_rootdir_path() == myrepo


def test_get_rootdir_path_while_in_subdir_two_deep(myrepo):
    """Returns root directory when called in sub-subdirectory of "myrepo"."""
    os.chdir(myrepo)
    assert Path(CONFIGFILE_NAME).exists()  # created by fixture "myrepo"
    os.chdir(os.path.join(myrepo, "a/b"))
    assert get_rootdir_path() == myrepo


def test_get_rootdir_path_while_in_subdir_three_deep(myrepo):
    """Returns root directory when called in sub-sub-subdirectory of "myrepo"."""
    os.chdir(myrepo)
    assert Path(CONFIGFILE_NAME).exists()  # created by fixture "myrepo"
    os.chdir(os.path.join(myrepo, "a/b/c"))
    assert get_rootdir_path() == myrepo


def test_get_rootdir_path_none_when_configfile_not_found(tmp_path):
    """Returns "None" as root directory in absence of config file."""
    os.chdir(tmp_path)
    Path("a/b/c").mkdir(parents=True, exist_ok=True)
    os.chdir("a/b/c")
    with pytest.raises(SystemExit):
        get_rootdir_path()


def test_get_rootdir_path_none_when_outside_repo(myrepo):
    """Returns "None" as root directory when called outside "myrepo"."""
    os.chdir(os.pardir)
    with pytest.raises(SystemExit):
        get_rootdir_path()
