"""@@@Docstring"""

import os
from mklists.utils import ls_visible


def test_ls_visible(tmpdir):
    """Test depends on get_lsvisible_names().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.mkdir("baz")
    assert ls_visible(tmpdir) == ["bar", "foo"]
