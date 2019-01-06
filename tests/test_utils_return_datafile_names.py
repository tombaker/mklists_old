"""@@@Docstring"""

import os
from mklists.utils import return_listfile_names, ls_visible_files


def test_return_listfile_names(tmpdir):
    """Test depends on ls_visible_files().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.mkdir("baz")
    files = ls_visible_files(tmpdir)
    assert return_listfile_names(files) == ["foo", "bar"]
