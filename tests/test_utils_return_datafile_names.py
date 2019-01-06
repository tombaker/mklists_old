"""@@@Docstring"""

import os
from mklists.utils import get_datafile_names, ls_visible_files


def test_get_datafile_names(tmpdir):
    """Test depends on ls_visible_files().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.mkdir("baz")
    files = ls_visible_files(tmpdir)
    assert get_datafile_names(files) == ["foo", "bar"]
