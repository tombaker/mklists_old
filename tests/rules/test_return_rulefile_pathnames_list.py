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


def test_return_rulefile_pathnames_chain_basic(tmp_path):
    """Typical: chain starts with rootdir, which has '.rules' file."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULES_CSVFILE_NAME,
    ]
    assert _return_rulefile_pathnames_chain(startdir_pathname=abc) == expected


def test_return_rulefile_pathnames_chain_ends_before_repo_rootdir(tmp_path):
    """Return chain starting below root directory (where rootdir has no '.rules')."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    # NOT Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULES_CSVFILE_NAME,
    ]
    assert _return_rulefile_pathnames_chain() == expected


def test_return_rulefile_pathnames_chain_even_without_repo_rootdir(tmp_path):
    """Specify startdir_pathname as argument instead of default (os.getcwd)."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    # NOT os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULES_CSVFILE_NAME,
    ]
    assert _return_rulefile_pathnames_chain(startdir_pathname=abc) == expected


def test_return_rulefile_pathnames_chain_without_specifying_startdir_pathname(tmp_path):
    """Return chain
    * called without specifying startdir_pathname as an argument
    * therefore defaults to current working directory as startdir_pathname"""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    os.chdir(abc)
    expected = [
        Path(tmp_path) / "a" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b" / RULES_CSVFILE_NAME,
        Path(tmp_path) / "a/b/c" / RULES_CSVFILE_NAME,
    ]
    assert _return_rulefile_pathnames_chain() == expected
