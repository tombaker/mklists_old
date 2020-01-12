"""
Returns repo root pathname when executed anywhere within repo.
* Starting at PWD, looks for:
    * mandatory CONFIG_YAMLFILE_NAME ('mklists.yml')
    * root directory - and if found, exit with error message

See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import os
import pytest
from mklists.config import Defaults

# pylint: disable=unused-argument
# These are just tests...

fixed = Defaults()

CONFIG_YAMLFILE_NAME = "mklists.yml"

RULE_CSVFILE_NAME = ".rules"

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
    # pylint: disable=unused-variable
    # Not a problem; this is just a fixture.
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    root_dir.join(CONFIG_YAMLFILE_NAME).write(TEST_CONFIG_YAMLFILE_STR)
    root_dir.join(RULE_CSVFILE_NAME).write(TEST_ROOTDIR_YAMLFILE_STR)
    subdir_a.join(RULE_CSVFILE_NAME).write(TEST_DATADIRA_YAMLFILE_STR)
    subdir_b = subdir_a.mkdir("b")
    subdir_c = subdir_b.mkdir("c")
    return root_dir


def test_return_rootdir_pathname_from_fixture_subdir(myrepo):
    """Find root pathname for fixture "myrepo"."""
    os.chdir(os.path.join(myrepo, "a"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert fixed.return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_while_in_rootdir_using_tmpdir(tmpdir):
    """Find root directory while in root directory."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    os.chdir(tmpdir)
    assert CONFIG_YAMLFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert fixed.return_rootdir_pathname() == str(tmpdir)


def test_return_rootdir_pathname_while_in_rootdir_using_fixture(myrepo):
    """Find root directory from subdirectory of root."""
    os.chdir(myrepo)
    assert CONFIG_YAMLFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert RULE_CSVFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert fixed.return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_while_in_subdir_two_deep(myrepo):
    """Find root directory while in subdir two deep."""
    os.chdir(os.path.join(myrepo, "a/b"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert fixed.return_rootdir_pathname() == str(myrepo)


def test_return_rootdir_pathname_while_in_subdir_three_deep(myrepo):
    """Find root directory while in subdir three deep."""
    os.chdir(os.path.join(myrepo, "a/b/c"))
    assert CONFIG_YAMLFILE_NAME in os.listdir(fixed.return_rootdir_pathname())
    assert fixed.return_rootdir_pathname() == str(myrepo)


def test_not_return_rootdir_pathname_when_configfile_not_found(tmpdir):
    """Do not find root directory when config file is not found."""
    tmpdira = tmpdir.mkdir("a")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirc = tmpdirb.mkdir("c")
    os.chdir(tmpdirc)
    assert os.getcwd() == str(tmpdirc)
    assert fixed.return_rootdir_pathname() is None


def test_not_return_rootdir_pathname_when_one_subdir_up(myrepo):
    """Do not find root directory when config file is is one subdir down."""
    os.chdir(os.pardir)
    assert fixed.return_rootdir_pathname() is None
