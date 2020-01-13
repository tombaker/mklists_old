"""@@@Docstring"""

import os
import pytest
from mklists.utils import return_datadir_pathnames_under_given_pathname
from mklists.config import CONFIG_YAMLFILE_NAME, RULES_CSVFILE_NAME, ROOTDIR_PATHNAME


def test_return_datadir_pathnames_under_given_pathname_excluding_rootdir(tmpdir):
    """List rulefile pathnames found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULES_CSVFILE_NAME).write("some rules")
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
    assert (
        return_datadir_pathnames_under_given_pathname(given_pathname=os.getcwd())
        == expected
    )


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


def test_return_datadir_pathnames_under_given_pathname_just_one(tmpdir):
    """List rulefile pathnames found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULES_CSVFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert return_datadir_pathnames_under_given_pathname() == expected


def test_return_datadir_pathnames_under_given_pathname_rootdir_has_no_rulefile(tmpdir):
    """List rulefile pathnames found under project root where
    there is no rulefile in the root directory itself."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULES_CSVFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert return_datadir_pathnames_under_given_pathname() == expected
