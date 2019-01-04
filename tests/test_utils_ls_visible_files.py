"""@@@Docstring"""

import os
from mklists.utils import ls_visible_files


def test_ls_visible_files(tmpdir):
    """Find root directory while in root directory."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff")
    tmpdir.join("bar").write("bar stuff")
    os.mkdir(tmpdir.join("baz"))
    assert "foo" in ls_visible_files(tmpdir)
    assert "bar" in ls_visible_files(tmpdir)
    assert "baz" not in ls_visible_files(tmpdir)
