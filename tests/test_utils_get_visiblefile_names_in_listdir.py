"""@@@Docstring"""

import os
from mklists.utils import get_visiblefile_names_in_listdir


def test_get_visiblefile_names_in_listdir(tmpdir):
    """Test depends on get_lsvisible_names().
    Directory 'a' should be ignored."""
    os.chdir(tmpdir)
    tmpdir.join("bar").write("bar stuff\nmore bar stuff")
    tmpdir.join("foo").write("foo stuff\nmore foo stuff")
    tmpdir.mkdir("baz")
    assert get_visiblefile_names_in_listdir(tmpdir) == ["bar", "foo"]
