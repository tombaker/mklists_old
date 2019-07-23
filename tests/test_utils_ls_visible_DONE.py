"""@@@Docstring"""

import os
from mklists.utils import ls_visiblefiles


def test_ls_visiblefiles(tmpdir):
    """Ignores directory baz."""
    os.chdir(tmpdir)
    tmpdir.join("bar").write("bar stuff")
    tmpdir.join("foo").write("foo stuff")
    tmpdir.mkdir("baz")
    assert ls_visiblefiles(tmpdir) == ["bar", "foo"]


def test_ls_visiblefiles_does_not_show_directories(tmpdir):
    """Ignores dot file."""
    os.chdir(tmpdir)
    tmpdir.join(".bar").write("bar stuff")
    tmpdir.join("foo").write("foo stuff")
    tmpdir.mkdir("baz")
    assert ls_visiblefiles(tmpdir) == ["foo"]
