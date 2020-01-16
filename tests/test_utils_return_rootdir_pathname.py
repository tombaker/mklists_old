"""Returns root pathname of mklists repo wherever executed in repo."""

import os
import pytest
from mklists.config import (
    CONFIG_YAMLFILE_NAME,
    RULES_CSVFILE_NAME,
    _return_rootdir_pathname,
)

# pylint: disable=unused-argument
# These are just tests...


@pytest.fixture(name="myrepo")
def fixture_myrepo(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    # pylint: disable=unused-variable
    # Not a problem; this is just a fixture.
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    root_dir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    root_dir.join(RULES_CSVFILE_NAME).write("rule stuff")
    subdir_a.join(RULES_CSVFILE_NAME).write("rule stuff")
    subdir_b = subdir_a.mkdir("b")
    subdir_c = subdir_b.mkdir("c")
    return root_dir


def test_return_rootdir_pathname_while_in_rootdir_using_tmpdir(tmpdir):
    """Returns root directory while already in root directory."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    assert CONFIG_YAMLFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert _return_rootdir_pathname() == str(tmpdir)


def test_return_rootdir_pathname_while_in_rootdir_using_fixture(myrepo):
    """Returns root directory starting in root directory of "myrepo"."""
    os.chdir(myrepo)
    assert CONFIG_YAMLFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert RULES_CSVFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert _return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_from_fixture_subdir(myrepo):
    """Returns root pathname starting in subdirectory of "myrepo"."""
    os.chdir(os.path.join(myrepo, "a"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert _return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_while_in_subdir_two_deep(myrepo):
    """Returns root directory starting in sub-subdirectory of "myrepo"."""
    os.chdir(os.path.join(myrepo, "a/b"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert _return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_while_in_subdir_three_deep(myrepo):
    """Returns root directory starting in sub-sub-subdirectory of "myrepo"."""
    os.chdir(os.path.join(myrepo, "a/b/c"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(_return_rootdir_pathname())
    assert _return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_none_when_configfile_not_found(tmpdir):
    """Returns "None" as root directory in absence of config file."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    assert os.getcwd() == str(tmpdirc)
    assert _return_rootdir_pathname() is None


def test_return_rootdir_pathname_none_when_outside_repo(myrepo):
    """Returns "None" as root directory when executed outside "myrepo"."""
    os.chdir(os.pardir)
    assert _return_rootdir_pathname() is None
