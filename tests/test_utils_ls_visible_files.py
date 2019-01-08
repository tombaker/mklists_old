"""@@@Docstring"""

import os
from mklists.utils import get_lsvisible_names


def test_get_lsvisible_names(tmpdir):
    """Find root directory while in root directory."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff")
    tmpdir.join("bar").write("bar stuff")
    os.mkdir(tmpdir.join("baz"))
    assert "foo" in get_lsvisible_names(tmpdir)
    assert "bar" in get_lsvisible_names(tmpdir)
    assert "baz" not in get_lsvisible_names(tmpdir)
