"""Return list of directories with .rules files under (but not including) root."""

import os
from pathlib import Path
from mklists.utils import return_data_subdirs_list
from mklists.constants import CONFIGFILE_NAME, DATADIR_RULEFILE_NAME


def test_return_data_subdirs_list__excluding_rootdir(tmp_path):
    """List data directories (ie, with rulefiles) under (but not including) root."""
    os.chdir(tmp_path)
    abc = Path.cwd().joinpath("a/b/c")
    abc.mkdir(parents=True, exist_ok=True)
    Path(CONFIGFILE_NAME).write_text("config stuff")
    Path(DATADIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b/c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path) / "a", Path(tmp_path) / "a/b", Path(tmp_path) / "a/b/c"]
    assert return_data_subdirs_list() == expected


def test_return_data_subdirs_list_ignoring_hidden_directory(tmp_path):
    """List data directories ignoring a "hidden" directory."""
    os.chdir(tmp_path)
    ab = Path.cwd().joinpath("a/b")
    ab.mkdir(parents=True, exist_ok=True)
    c = Path.cwd().joinpath("c")
    c.mkdir()
    hidden = Path.cwd().joinpath(".hidden")
    hidden.mkdir()
    Path(CONFIGFILE_NAME).write_text("config stuff")
    Path(DATADIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("a/b", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath("c", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    Path(tmp_path).joinpath(".hidden", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path) / "a", Path(tmp_path) / "a/b", Path(tmp_path) / "c"]
    assert return_data_subdirs_list() == expected


def test_return_data_subdirs_list_just_one(tmp_path):
    """List data directories when there is just one."""
    os.chdir(tmp_path)
    a = Path("a")
    a.mkdir()
    Path(CONFIGFILE_NAME).write_text("config stuff")
    Path(DATADIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path).joinpath("a")]
    assert return_data_subdirs_list() == expected


def test_return_data_subdirs_list_rootdir_has_no_rulefile(tmp_path):
    """List data directories even when root directory has no rulefile."""
    os.chdir(tmp_path)
    a = Path("a")
    a.mkdir()
    Path(CONFIGFILE_NAME).write_text("config stuff")
    # NOT Path(DATADIR_RULEFILE_NAME).write_text("rule stuff")
    Path(tmp_path).joinpath("a", DATADIR_RULEFILE_NAME).write_text("rule_stuff")
    expected = [Path(tmp_path).joinpath("a")]
    assert return_data_subdirs_list() == expected
