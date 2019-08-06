"""@@@Docstring"""

import os
from mklists.utils import return_visiblefiles_list


def test_return_visiblefiles_list(tmpdir):
    """Ignores directory 'baz'."""
    os.chdir(tmpdir)
    tmpdir.join("bar").write("bar stuff")
    tmpdir.join("foo").write("foo stuff")
    tmpdir.mkdir("baz")
    assert return_visiblefiles_list(tmpdir) == ["bar", "foo"]


def test_return_visiblefiles_list_does_not_show_directories(tmpdir):
    """Ignores dot file '.bar'."""
    os.chdir(tmpdir)
    tmpdir.join(".bar").write("bar stuff")
    tmpdir.join("foo").write("foo stuff")
    assert return_visiblefiles_list(tmpdir) == ["foo"]