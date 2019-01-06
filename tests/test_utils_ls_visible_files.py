"""@@@Docstring"""

import os
from mklists.utils import return_visiblefile_names


def test_return_visiblefile_names(tmpdir):
    """Find root directory while in root directory."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff")
    tmpdir.join("bar").write("bar stuff")
    os.mkdir(tmpdir.join("baz"))
    assert "foo" in return_visiblefile_names(tmpdir)
    assert "bar" in return_visiblefile_names(tmpdir)
    assert "baz" not in return_visiblefile_names(tmpdir)
