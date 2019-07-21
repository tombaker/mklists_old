"""Return repo root pathname when executed anywhere within repo.

    Look for mandatory file CONFIG_YAMLFILE_NAME ('mklists.yml').

    Starting at PWD, should look for:
    * file 'mklists.yml' - and if found, return full pathname
    * root directory - and if found, exit with error message

See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""


import os
import pytest
from mklists.initialize import CONFIG_YAMLFILE_NAME
from mklists.utils import get_rootdir_pathname


def test_get_rootdir_pathname_from_fixture_subdir(myrepo):
    """Find root pathname for fixture "myrepo"."""
    os.chdir(os.path.join(myrepo, "a"))
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname(cwd=curdir))


def test_get_rootdir_pathname_while_in_rootdir(tmpdir):
    """Find root directory while in root directory."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname(cwd=curdir))


def test_get_rootdir_pathname_while_in_subdir_one_deep(tmpdir):
    """Find root directory from subdirectory of root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    os.chdir(tmpdira)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname(cwd=curdir))


def test_get_rootdir_pathname_while_in_subdir_two_deep(tmpdir):
    """Find root directory while in subdir two deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    os.chdir(tmpdirb)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname(cwd=curdir))


def test_get_rootdir_pathname_while_in_subdir_three_deep(tmpdir):
    """Find root directory while in subdir three deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname(cwd=curdir))


def test_not_get_rootdir_pathname_when_configfile_not_found(tmpdir):
    """Do not find root directory when config file is not found."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    curdir = os.getcwd()
    with pytest.raises(SystemExit):
        get_rootdir_pathname(cwd=curdir)
