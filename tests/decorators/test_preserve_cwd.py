"""Tests for decorator @preserve_cwd"""

import os
from pathlib import Path
from mklists.decorators import preserve_cwd


def test_preserve_cwd(tmp_path):
    """@@@Docstring"""
    os.chdir(tmp_path)
    directory_before = Path.cwd()
    tmpdir_some_directory = Path(tmp_path) / "some_directory"
    Path(tmpdir_some_directory).mkdir()

    @preserve_cwd
    def change_directory_to(change_to=None):
        os.chdir(change_to)
        return Path.cwd()

    directory_returned = change_directory_to(tmpdir_some_directory)
    directory_after = Path.cwd()

    assert tmpdir_some_directory == directory_returned
    assert directory_after == directory_before
