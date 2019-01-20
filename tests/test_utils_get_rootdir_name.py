"""@@@Docstring"""

import os
import pytest
from mklists.constants import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from mklists.utils import get_rootdir_name


def test_get_rootdir_name_from_fixture_subdir(myrepo):
    """Find root directory from root directory of fixture."""
    os.chdir(os.path.join(myrepo, "a"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_name())


def test_get_rootdir_name_while_in_rootdir(tmpdir):
    """Find root directory while in root directory."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_name())


def test_get_rootdir_name_while_in_subdir_one_deep(tmpdir):
    """Find root directory while in subdir one deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    os.chdir(tmpdira)
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_name())


def test_get_rootdir_name_while_in_subdir_two_deep(tmpdir):
    """Find root directory while in subdir two deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some more rules")
    os.chdir(tmpdirb)
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_name())


def test_get_rootdir_name_while_in_subdir_three_deep(tmpdir):
    """Find root directory while in subdir three deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some more rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("still more rules")
    os.chdir(tmpdirc)
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_name())


def test_not_get_rootdir_name_given_missing_link(tmpdir):
    """Do not find root directory when rulefile chain has missing link."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join("foobar").write("some more rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("still more rules")
    os.chdir(tmpdirc)
    with pytest.raises(SystemExit):
        get_rootdir_name()


# @pytest.mark.skip
# def test_write_initial_config_yamlfile(tmpdir):
#     """Write mklists.yml, then read it back."""
#     os.chdir(tmpdir)
#     mklistsrc = tmpdir.join(CONFIG_YAMLFILE_NAME)
#     _write_initial_config_yamlfile(config_yamlfile_name=mklistsrc)
#     updated_context = _apply_overrides_from_file()
#     assert (
#        updated_context["valid_filename_characters"] == VALID_FILENAME_CHARACTERS_REGEX
#     )
