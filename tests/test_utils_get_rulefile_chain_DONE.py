"""See
/Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import os
import pytest
from mklists.initialize import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
from mklists.utils import get_rootdir_pathname, get_rulefile_chain, preserve_cwd


def test_get_rulefile_chain_basic(tmpdir):
    """Normal case: happens to end in rootdir (with 'mklists.yml' file)."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    expected = [
        os.path.join(tmpdir, ".rules"),
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
    ]
    assert get_rulefile_chain(start_pathname=tmpdirc) == expected


def test_get_rulefile_chain_ends_before_repo_rootdir(tmpdir):
    """Chain of directories with '.rules' ends before repo rootdir."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    expected = [
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
    ]
    assert get_rulefile_chain(start_pathname=tmpdirc) == expected


def test_get_rulefile_chain_even_without_repo_rootdir(tmpdir):
    """Shows that get_rulefile_chain() does not test whether
    start_pathname is in a mklists repo."""
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    expected = [
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
    ]
    assert get_rulefile_chain(start_pathname=tmpdirc) == expected


def test_get_rulefile_chain_without_specifying_start_pathname(tmpdir):
    """Shows that get_rulefile_chain() does not test whether
    start_pathname is in a mklists repo."""
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    os.chdir(tmpdirc)
    expected = [
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
    ]
    print(os.getcwd())
    assert get_rulefile_chain() == expected
