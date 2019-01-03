"""@@@Docstring"""

import os
import pytest
from mklists.utils import find_project_root
from mklists import CONFIGFILE_NAME, LOCAL_RULEFILE_NAME, RULEFILE_NAME


def test_find_project_root_while_in_rootdir(tmpdir):
    """Find root directory while in root directory."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    assert CONFIGFILE_NAME in os.listdir(find_project_root())


def test_find_project_root_while_in_subdir_one_deep(tmpdir):
    """Find root directory while in subdir one deep."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    os.chdir(tmpdira)
    assert CONFIGFILE_NAME in os.listdir(find_project_root())


def test_find_project_root_while_in_subdir_two_deep(tmpdir):
    """Find root directory while in subdir two deep."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULEFILE_NAME).write("some more rules")
    os.chdir(tmpdirb)
    assert CONFIGFILE_NAME in os.listdir(find_project_root())


def test_find_project_root_while_in_subdir_three_deep(tmpdir):
    """Find root directory while in subdir three deep."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULEFILE_NAME).write("some more rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(LOCAL_RULEFILE_NAME).write("still more rules")
    os.chdir(tmpdirc)
    assert CONFIGFILE_NAME in os.listdir(find_project_root())


def test_not_find_project_root_given_missing_link(tmpdir):
    """Do not find root directory when rulefile chain has missing link."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join("foobar").write("some more rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(LOCAL_RULEFILE_NAME).write("still more rules")
    os.chdir(tmpdirc)
    with pytest.raises(SystemExit):
        find_project_root()


# @pytest.mark.skip
# def test_write_initial_configfile(tmpdir):
#     """Write mklists.yml, then read it back."""
#     os.chdir(tmpdir)
#     mklistsrc = tmpdir.join(CONFIGFILE_NAME)
#     _write_initial_configfile(configfile_name=mklistsrc)
#     updated_context = _apply_overrides_from_file()
#     assert (
#        updated_context["valid_filename_characters"] == VALID_FILENAME_CHARACTERS_REGEX
#     )
