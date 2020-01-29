"""Return list of rule file pathnames."""

import os
from pathlib import Path
from mklists.rules import _return_parent_rulefile_paths
from mklists.constants import CONFIG_YAMLFILE_NAME

RULEFILE_NAME = ".rules"


# 2019-01-19:
# TODO: Possible developments:
#  Could generate one big dictionary of rulefile chains for entire repo
#  Test: function stops looking for '.rules' above rootdir (i.e., 'mklists.yml' found).


def test_return_parent_rulefile_paths_typical(tmp_path):
    """Typical: chain starts with rootdir, which has '.rules' file."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / RULEFILE_NAME,
        Path(tmp_path) / "a" / RULEFILE_NAME,
        Path(tmp_path) / "a/b" / RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths(startdir_path=abc) == expected


def test_return_parent_rulefile_paths_ends_before_repo_rootdir(tmp_path):
    """Return chain starting below root directory (where rootdir has no '.rules')."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    # NOT Path(RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULEFILE_NAME,
        Path(tmp_path) / "a/b" / RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths() == expected


def test_return_parent_rulefile_paths_without_specifying_rootdir(tmp_path):
    """Specify startdir_path as argument instead of default (os.getcwd)."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(tmp_path).joinpath("a", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULEFILE_NAME).write_text("rule_stuff")
    # NOT os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULEFILE_NAME,
        Path(tmp_path) / "a/b" / RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths(startdir_path=abc) == expected


def test_return_parent_rulefile_paths_without_specifying_startdir_path(tmp_path):
    """Return chain
    * called without specifying startdir_path as an argument
    * therefore defaults to current working directory as startdir_path"""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(tmp_path).joinpath("a", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULEFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULEFILE_NAME,
        Path(tmp_path) / "a/b" / RULEFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULEFILE_NAME,
    ]
    assert _return_parent_rulefile_paths() == expected
