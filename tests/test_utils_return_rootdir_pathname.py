"""
Returns repo root pathname when executed anywhere within repo.
* Starting at PWD, looks for:
    * mandatory CONFIG_YAMLFILE_NAME ('mklists.yml')
    * root directory - and if found, exit with error message

See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import os
import pytest
from mklists.initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from mklists.utils import return_rootdir_pathname


TEST_CONFIG_YAMLFILE_STR = r"""\
invalid_filename_patterns: ['\.swp$', '\.tmp$', '~$', '^\.']
"""

TEST_ROOTDIR_YAMLFILE_STR = """\
- [0, '.', all, lines, 0]
"""

TEST_DATADIRA_YAMLFILE_STR = """\
- [2, 'NOW',     lines,  now,     1]
- [2, 'LATER',   lines,  later,   0]
"""


@pytest.fixture(name="myrepo")
def fixture_myrepo(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    root_dir.join(CONFIG_YAMLFILE_NAME).write(TEST_CONFIG_YAMLFILE_STR)
    root_dir.join(CONFIG_YAMLFILE_NAME).write(TEST_ROOTDIR_YAMLFILE_STR)
    subdir_a.join(RULE_YAMLFILE_NAME).write(TEST_DATADIRA_YAMLFILE_STR)
    return root_dir


def test_return_rootdir_pathname_from_fixture_subdir(myrepo):
    """Find root pathname for fixture "myrepo"."""
    os.chdir(os.path.join(myrepo, "a"))
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(
        return_rootdir_pathname(_currentdir_pathname=curdir)
    )


def test_return_rootdir_pathname_while_in_rootdir(tmpdir):
    """Find root directory while in root directory."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(
        return_rootdir_pathname(_currentdir_pathname=curdir)
    )


def test_return_rootdir_pathname_while_in_subdir_one_deep(tmpdir):
    """Find root directory from subdirectory of root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    os.chdir(tmpdira)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(
        return_rootdir_pathname(_currentdir_pathname=curdir)
    )


def test_return_rootdir_pathname_while_in_subdir_two_deep(tmpdir):
    """Find root directory while in subdir two deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    os.chdir(tmpdirb)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(
        return_rootdir_pathname(_currentdir_pathname=curdir)
    )


def test_return_rootdir_pathname_while_in_subdir_three_deep(tmpdir):
    """Find root directory while in subdir three deep."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    curdir = os.getcwd()
    assert CONFIG_YAMLFILE_NAME in os.listdir(
        return_rootdir_pathname(_currentdir_pathname=curdir)
    )


def test_not_return_rootdir_pathname_when_configfile_not_found(tmpdir):
    """Do not find root directory when config file is not found."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    curdir = os.getcwd()
    with pytest.raises(SystemExit):
        return_rootdir_pathname(_currentdir_pathname=curdir)
