"""See
/Users/tbaker/github/tombaker/mklists/mklists/utils.py

$ mklists run (the default)
  * For all datadirs
    * Change to datadir
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
from mklists.initialize import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
from mklists.utils import return_rulefile_pathnames_chain_as_list


def test_return_rulefile_pathnames_chain_as_list_basic(tmpdir):
    """Here: the normal case: sequence of directories with '.rules'
    ends in rootdir (which also has 'mklists.yml' file)."""
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
    assert (
        return_rulefile_pathnames_chain_as_list(_startdir_pathname=tmpdirc) == expected
    )


def test_return_rulefile_pathnames_chain_as_list_ends_before_repo_rootdir(tmpdir):
    """Here: sequence of directories with ".rules" ends
    before reaching root directory of repo (i.e., the
    root directory does not itself have a ".rules" file."""
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
    assert (
        return_rulefile_pathnames_chain_as_list(_startdir_pathname=tmpdirc) == expected
    )


def test_return_rulefile_pathnames_chain_as_list_even_without_repo_rootdir(tmpdir):
    """Here: return_rulefile_pathnames_chain_as_list()
    called with _startdir_pathname as an argument."""
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
    assert (
        return_rulefile_pathnames_chain_as_list(_startdir_pathname=tmpdirc) == expected
    )


def test_return_rulefile_pathnames_chain_as_list_without_specifying_startdir_pathname(
    tmpdir
):
    """Here: return_rulefile_pathnames_chain_as_list()
    * called without specifying _startdir_pathname as an argument
    * therefore defaults to current working directory as _startdir_pathname"""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
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
    assert return_rulefile_pathnames_chain_as_list() == expected
