"""@@@Docstring"""

import os
from mklists import CONFIGFILE_NAME, RULEFILE_NAME
from mklists.utils import get_listdir_names_under_rootdir


def test_get_listdir_names_under_rootdir(tmpdir):
    """List data directories found under project root."""
    tmpdir.join(CONFIGFILE_NAME).write("config stuff")
    tmpdira = tmpdir.mkdir("a")
    tmpdira.join(RULEFILE_NAME).write("some rules")
    tmpdirb = tmpdira.mkdir("b")
    tmpdirb.join(RULEFILE_NAME).write("some more rules")
    os.chdir(tmpdir)
    expected = [os.path.join(tmpdir, "a"), os.path.join(tmpdir, "a/b")]
    assert get_listdir_names_under_rootdir(tmpdir) == expected
