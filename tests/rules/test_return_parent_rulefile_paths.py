"""Return list of rule file pathnames."""

import os
from pathlib import Path
from mklists.rules import _return_parent_rulefile_paths
from mklists.constants import (
    CONFIG_YAMLFILE_NAME,
    ROOTDIR_RULEFILE_NAME,
    DATADIR_RULEFILE_NAME,
)


# 2019-01-19:
# TODO: Possible developments:
#  Could generate one big dictionary of rulefile chains for entire repo
#  Test: function stops looking for '.rules' above rootdir (i.e., 'mklists.yml' found).


def test_return_parent_rulefile_paths_typical(tmp_path):
    """Return list of rulefiles from root to (current) working data directory."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(Path(tmp_path).joinpath("a/b/c"))
    expected = [
        Path(tmp_path) / ROOTDIR_RULEFILE_NAME,
        Path(tmp_path) / "a" / DATADIR_RULEFILE_NAME,
        Path(tmp_path) / "a/b" / DATADIR_RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / DATADIR_RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths(startdir=abc) == expected


def test_return_parent_rulefile_paths_ends_before_repo_rootdir(tmp_path):
    """Return list of data directory rulefiles only when 'rules.cfg' not reachable)."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / "a/b" / DATADIR_RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / DATADIR_RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths() == expected


def test_return_parent_rulefile_paths_with_specifying_rootdir(tmp_path):
    """Return correct list when starting directory is explicitly specified."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    expected = [
        Path(tmp_path) / ROOTDIR_RULEFILE_NAME,
        Path(tmp_path) / "a" / DATADIR_RULEFILE_NAME,
        Path(tmp_path) / "a/b" / DATADIR_RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / DATADIR_RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths(startdir=abc) == expected


def test_return_parent_rulefile_paths_empty_list_when_starting_in_non_datadir(tmp_path):
    """Return empty list when starting in a non-data directory."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    d = Path.cwd().joinpath("d")
    abc.mkdir(parents=True, exist_ok=True)
    d.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(d)
    expected = []
    assert _return_parent_rulefile_paths() == expected


def test_return_parent_rulefile_paths_empty_list_when_starting_in_rootdir(tmp_path):
    """Return empty list when starting in root directory."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(ROOTDIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(tmp_path)
    expected = []
    assert _return_parent_rulefile_paths() == expected
