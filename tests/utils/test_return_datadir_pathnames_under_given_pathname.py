"""Return list of directories with .rules files under (but not including) root."""

import os
from pathlib import Path
from mklists.utils import return_datadir_pathnames_under_given_pathname
from mklists.constants import CONFIG_YAMLFILE_NAME, RULES_CSVFILE_NAME


def test_return_datadir_pathnames_under_given_pathname_excluding_rootdir(tmp_path):
    """List data directories (ie, with rulefiles) under (but not including) root."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path) / "a", Path(tmp_path) / "a/b", Path(tmp_path) / "a/b/c"]
    assert return_datadir_pathnames_under_given_pathname() == expected


def test_return_datadir_pathnames_under_given_pathname_excluding_hiddendirs(tmp_path):
    """List data directories ignoring a "hidden" directory."""
    os.chdir(tmp_path)
    ab = Path.cwd().joinpath("a/b")
    ab.mkdir(parents=True, exist_ok=True)
    c = Path.cwd().joinpath("c")
    c.mkdir()
    hidden = Path.cwd().joinpath(".hidden")
    hidden.mkdir()
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("c", RULES_CSVFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath(".hidden", RULES_CSVFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path) / "a", Path(tmp_path) / "a/b", Path(tmp_path) / "c"]
    assert return_datadir_pathnames_under_given_pathname() == expected


def test_return_datadir_pathnames_under_given_pathname_just_one(tmp_path):
    """List data directories when there is just one."""
    os.chdir(tmp_path)
    a = Path("a")
    a.mkdir()
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path).joinpath("a")]
    assert return_datadir_pathnames_under_given_pathname() == expected


def test_return_datadir_pathnames_under_given_pathname_rootdir_has_no_rulefile(
    tmp_path
):
    """List data directories even when root directory has no rulefile."""
    os.chdir(tmp_path)
    a = Path("a")
    a.mkdir()
    Path(CONFIG_YAMLFILE_NAME).write_text("config stuff")
    # NOT Path(RULES_CSVFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", RULES_CSVFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path).joinpath("a")]
    assert return_datadir_pathnames_under_given_pathname() == expected
