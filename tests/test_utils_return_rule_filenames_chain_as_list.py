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

. Tree 1: top is '/'
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

. Tree 2: top is '/detached'
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
from mklists.utils import (
    return_rootdir_pathname,
    return_rule_filenames_chain_as_list,
    preserve_cwd,
)


def test_return_rule_filenames_chain_as_list_basic(tmpdir):
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
    assert return_rule_filenames_chain_as_list(_startdir_pathname=tmpdirc) == expected


def test_return_rule_filenames_chain_as_list_ends_before_repo_rootdir(tmpdir):
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
    assert return_rule_filenames_chain_as_list(_startdir_pathname=tmpdirc) == expected


def test_return_rule_filenames_chain_as_list_even_without_repo_rootdir(tmpdir):
    """Shows that return_rule_filenames_chain_as_list() does not test whether
    _startdir_pathname is in a mklists repo."""
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
    assert return_rule_filenames_chain_as_list(_startdir_pathname=tmpdirc) == expected


def test_return_rule_filenames_chain_as_list_without_specifying_startdir_pathname(
    tmpdir
):
    """Shows that return_rule_filenames_chain_as_list() does not test whether
    _startdir_pathname is in a mklists repo."""
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
    assert return_rule_filenames_chain_as_list() == expected
