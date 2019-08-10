"""@@@Docstring"""

import os
from mklists.initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from mklists.utils import return_datadir_pathnames_under_somedir


def test_return_datadir_pathnames_under_somedir_excluding_rootdir(tmpdir):
    """List rulefile pathnames found under project root."""
    rootdir_pathname = tmpdir
    rule_yamlfile_name = RULE_YAMLFILE_NAME
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(rule_yamlfile_name).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(rule_yamlfile_name).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(rule_yamlfile_name).write("some rules")
    tmpdirc = tmpdir.mkdir("c")
    tmpdirc.join(rule_yamlfile_name).write("some rules")
    os.chdir(tmpdir)
    expected = [
        os.path.join(tmpdir, "a"),
        os.path.join(tmpdir, "a/b"),
        os.path.join(tmpdir, "c"),
    ]
    assert (
        return_datadir_pathnames_under_somedir(
            _rootdir_pathname=rootdir_pathname,
            _somedir_pathname=tmpdir,
            _rule_yamlfile_name=rule_yamlfile_name,
        )
        == expected
    )


def test_return_datadir_pathnames_under_somedir_excluding_hiddendirs(tmpdir):
    """List rulefile pathnames found under project root."""
    rootdir_pathname = tmpdir
    rule_yamlfile_name = RULE_YAMLFILE_NAME
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(rule_yamlfile_name).write("some rules")
    tmpdir_hidden = tmpdir.mkdir(".hidden")
    tmpdir_hidden.join(rule_yamlfile_name).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(rule_yamlfile_name).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(rule_yamlfile_name).write("some rules")
    tmpdirc = tmpdir.mkdir("c")
    tmpdirc.join(rule_yamlfile_name).write("some rules")
    os.chdir(tmpdir)
    expected = [
        os.path.join(tmpdir, "a"),
        os.path.join(tmpdir, "a/b"),
        os.path.join(tmpdir, "c"),
    ]
    assert (
        return_datadir_pathnames_under_somedir(
            _rootdir_pathname=rootdir_pathname,
            _somedir_pathname=tmpdir,
            _rule_yamlfile_name=rule_yamlfile_name,
        )
        == expected
    )


def test_return_datadir_pathnames_under_somedir_just_one(tmpdir):
    """List rulefile pathnames found under project root."""
    rootdir_pathname = tmpdir
    rule_yamlfile_name = RULE_YAMLFILE_NAME
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdir.join(rule_yamlfile_name).write("some rules")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(rule_yamlfile_name).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert (
        return_datadir_pathnames_under_somedir(
            _rootdir_pathname=rootdir_pathname,
            _somedir_pathname=tmpdir,
            _rule_yamlfile_name=rule_yamlfile_name,
        )
        == expected
    )


def test_return_datadir_pathnames_under_somedir_rootdir_has_no_rulefile(tmpdir):
    """List rulefile pathnames found under project root where
    there is no rulefile in the root directory itself."""
    rootdir_pathname = tmpdir
    rule_yamlfile_name = RULE_YAMLFILE_NAME
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(rule_yamlfile_name).write("some rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a")]
    assert (
        return_datadir_pathnames_under_somedir(
            _rootdir_pathname=rootdir_pathname,
            _somedir_pathname=tmpdir,
            _rule_yamlfile_name=rule_yamlfile_name,
        )
        == expected
    )
