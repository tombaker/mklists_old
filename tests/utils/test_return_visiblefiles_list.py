"""@@@Docstring"""

import os
from pathlib import Path
from mklists.utils import return_visiblefiles_list


def test_return_visiblefiles_list(tmp_path):
    """Ignores directory 'baz'."""
    os.chdir(tmp_path)
    Path("bar").write_text("bar stuff")
    Path("foo").write_text("foo stuff")
    Path("baz").mkdir()
    assert return_visiblefiles_list() == ["bar", "foo"]
    assert Path.cwd() == Path(tmp_path)


def test_return_visiblefiles_list_does_not_show_directories(tmp_path):
    """Ignores dot file '.bar'."""
    os.chdir(tmp_path)
    Path(".bar").write_text("bar stuff")
    Path("foo").write_text("foo stuff")
    assert return_visiblefiles_list() == ["foo"]
