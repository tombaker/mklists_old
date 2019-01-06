"""@@@Docstring"""

import os
from mklists import CONFIGFILE_NAME, LOCAL_RULEFILE_NAME, RULEFILE_NAME
from mklists.utils import return_datadirs_under_project_rootdir


def test_return_datadirs_under_project_rootdir(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULEFILE_NAME).write("some more rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a"), os.path.join(tmpdir, "a/b")]
    assert return_datadirs_under_project_rootdir(tmpdir) == expected


def test_return_datadirs_under_project_rootdir_with_localrules(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(LOCAL_RULEFILE_NAME).write("some local rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULEFILE_NAME).write("some more rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a"), os.path.join(tmpdir, "a/b")]
    assert return_datadirs_under_project_rootdir(tmpdir) == expected
