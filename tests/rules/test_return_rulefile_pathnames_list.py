"""Return list of rule file pathnames."""

import os
from pathlib import Path
from mklists.rules import _return_rulefile_pathnames_chain
from mklists.constants import CONFIG_YAMLFILE_NAME

RULES_CSVFILE_NAME = ".rules"


# 2019-01-19:
# TODO: Possible developments:
#  Could generate one big dictionary of rulefile chains for entire repo
#  Test: function stops looking for '.rules' above rootdir (i.e., 'mklists.yml' found).


def test_return_rulefile_pathnames_chain_basic(tmpdir):
    """Typical: chain starts with rootdir, which has '.rules' file."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULES_CSVFILE_NAME).write("rule stuff")
    expected = [
        Path(tmpdir) / ".rules",
        Path(tmpdir) / "a/.rules",
        Path(tmpdir) / "a/b/.rules",
        Path(tmpdir) / "a/b/c/.rules",
    ]
    assert _return_rulefile_pathnames_chain(startdir_pathname=tmpdirc) == expected


def test_return_rulefile_pathnames_chain_ends_before_repo_rootdir(tmpdir):
    """Return chain starting below root directory (where rootdir has no '.rules')."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULES_CSVFILE_NAME).write("rule stuff")
    os.chdir(tmpdirc)
    expected = [
        Path(tmpdir) / "a/.rules",
        Path(tmpdir) / "a/b/.rules",
        Path(tmpdir) / "a/b/c/.rules",
    ]
    assert _return_rulefile_pathnames_chain() == expected


def test_return_rulefile_pathnames_chain_even_without_repo_rootdir(tmpdir):
    """Specify startdir_pathname as argument instead of default (os.getcwd)."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULES_CSVFILE_NAME).write("rule stuff")
    expected = [
        Path(tmpdir) / "a/.rules",
        Path(tmpdir) / "a/b/.rules",
        Path(tmpdir) / "a/b/c/.rules",
    ]
    assert _return_rulefile_pathnames_chain(startdir_pathname=tmpdirc) == expected


def test_return_rulefile_pathnames_chain_without_specifying_startdir_pathname(tmpdir):
    """Return chain
    * called without specifying startdir_pathname as an argument
    * therefore defaults to current working directory as startdir_pathname"""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULES_CSVFILE_NAME).write("rule stuff")
    tmpdirc = tmpdirb.mkdir("c")
    tmpdirc.join(RULES_CSVFILE_NAME).write("rule stuff")
    os.chdir(tmpdirc)
    expected = [
        Path(tmpdira) / ".rules",
        Path(tmpdirb) / ".rules",
        Path(tmpdirc) / ".rules",
    ]
    assert _return_rulefile_pathnames_chain() == expected
