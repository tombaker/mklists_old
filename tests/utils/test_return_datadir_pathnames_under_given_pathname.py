"""Return list of directories with .rules files under (but not including) root."""

import os
import pytest
from pathlib import Path
from mklists.utils import return_datadir_pathnames_under_given_pathname
from mklists.constants import CONFIG_YAMLFILE_NAME, RULES_CSVFILE_NAME


def test_return_datadir_pathnames_under_given_pathname_excluding_rootdir(tmp_path):
    """List directories with rule files under (but not including) root directory."""
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


@pytest.mark.skip
def test_return_datadir_pathnames_under_given_pathname_excluding_hiddendirs(tmpdir):
    """List rulefile pathnames found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdir_hidden = tmpdir.mkdir(".hidden")
    tmpdir_hidden.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdirc = tmpdir.mkdir("c")
    tmpdirc.join(RULES_CSVFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [
        os.path.join(tmpdir, "a"),
        os.path.join(tmpdir, "a/b"),
        os.path.join(tmpdir, "c"),
    ]
    assert return_datadir_pathnames_under_given_pathname() == expected


@pytest.mark.skip
def test_return_datadir_pathnames_under_given_pathname_just_one(tmpdir):
    """List rulefile pathnames found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert return_datadir_pathnames_under_given_pathname() == expected


@pytest.mark.skip
def test_return_datadir_pathnames_under_given_pathname_rootdir_has_no_rulefile(tmpdir):
    """List rulefile pathnames found under project root where
    there is no rulefile in the root directory itself."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert return_datadir_pathnames_under_given_pathname() == expected
