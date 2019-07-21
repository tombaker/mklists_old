"""@@@Docstring"""

import os
from mklists.initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from mklists.utils import get_datadir_pathnames_under_rootdir


def test_get_datadir_pathnames_under_rootdir(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdir.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [
        tmpdir,
        os.path.join(tmpdir, "a"),
        os.path.join(tmpdir, "a/b"),
        os.path.join(tmpdir, "c"),
    ]
    assert get_datadir_pathnames_under_rootdir(tmpdir) == expected


def test_get_datadir_pathnames_under_rootdir_excluding_hiddendirs(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdir_hidden = tmpdir.mkdir(".hidden")
    tmpdir_hidden.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULE_YAMLFILE_NAME).write("some rules")
    tmpdirc = tmpdir.mkdir("c")
    tmpdirc.join(RULE_YAMLFILE_NAME).write("some rules")
    os.chdir(tmpdir)
    expected = [
        tmpdir,
        os.path.join(tmpdir, "a"),
        os.path.join(tmpdir, "a/b"),
        os.path.join(tmpdir, "c"),
    ]
    assert get_datadir_pathnames_under_rootdir(tmpdir) == expected
