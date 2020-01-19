"""See
/Users/tbaker/github/tombaker/mklists/mklists/utils.py

$ mklists run (the default)
  * For all datadirs
    * Change to rootdir
      * Run mklists, using
        * rules from current directory
        * rules from parent directories, if available - stopping at root

$ mklists run --here
  * For current datadir
      * Run mklists, using
        * rules from current directory
        * rules from parent directories, if available - stopping at root
  * If run in root directory, will exit with: "No data to process!".

. Tree 1: top is '/' (i.e., root directory of the _repo_)
├── .rules                    $ mklists run --here: "No data to process!"
├── a                         $ mklists run --here: uses /.rules a/.rules
│   ├── .rules                $
│   ├── a1                    $ mklists run --here: uses /.rules a/.rules a/a1/.rules
│   │   ├── .rules
│   │   └── c                 $ mklists run --here: uses /.rules a/.rules a/a1/.rules a/a1/c/.rules
│   │       └── .rules        $
│   └── a2                    $
│       └── .rules            $
├── b                         $ mklists run --here: uses /.rules b/.rules
│   └── .rules                $

. Tree 2: top is '/detached' (i.e., subdirectory under the root directory of the _repo_)
├── detached                  $ mklists run --here: uses detached/.rules: "No data to process!"
│   ├── .rules                $
│   ├── e                     $ mklists run --here: uses detached/.rules e/.rules
│   │   └── .rules            $
│   └── f                     $ mklists run --here: uses detached/.rules f/.rules
│       └── .rules            $
└── mklists.yml
"""

import os
import pytest
from mklists.rules import Rule, _return_rulefile_pathnames_chain
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
        os.path.join(tmpdir, ".rules"),
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
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
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
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
        os.path.join(tmpdir, "a/.rules"),
        os.path.join(tmpdir, "a/b/.rules"),
        os.path.join(tmpdir, "a/b/c/.rules"),
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
        os.path.join(tmpdira, ".rules"),
        os.path.join(tmpdirb, ".rules"),
        os.path.join(tmpdirc, ".rules"),
    ]
    assert _return_rulefile_pathnames_chain() == expected
