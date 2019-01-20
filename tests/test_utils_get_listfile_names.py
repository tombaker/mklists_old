"""@@@Docstring"""

import os
from mklists.utils import get_listfile_names


def test_get_listfile_names(tmpdir):
    """Test depends on get_lsvisible_names().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.mkdir("baz")
    assert get_listfile_names(tmpdir) == ["foo", "bar"]