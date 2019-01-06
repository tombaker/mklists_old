"""@@@Docstring"""

import os
from mklists.utils import return_listfile_names, return_visiblefile_names


def test_return_listfile_names(tmpdir):
    """Test depends on return_visiblefile_names().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.mkdir("baz")
    files = return_visiblefile_names(tmpdir)
    assert return_listfile_names(files) == ["foo", "bar"]
