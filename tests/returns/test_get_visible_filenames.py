"""@@@Docstring"""

import os
from pathlib import Path
from mklists.returns import get_visible_filenames


def test_get_visible_filenames(tmp_path):
    """Ignores directory 'baz'."""
    os.chdir(tmp_path)
    Path("bar").write_text("bar stuff")
    Path("foo").write_text("foo stuff")
    Path("baz").mkdir()
    assert get_visible_filenames() == ["bar", "foo"]
    assert Path.cwd() == Path(tmp_path)


def test_get_visible_filenames_does_not_show_directories(tmp_path):
    """Ignores dot file '.bar'."""
    os.chdir(tmp_path)
    Path(".bar").write_text("bar stuff")
    Path("foo").write_text("foo stuff")
    assert get_visible_filenames() == ["foo"]
