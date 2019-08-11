"""Tests for decorator @preserve_cwd

Edit /Users/tbaker/github/tombaker/mklists/mklists/decorators.py
"""

import os
from mklists.decorators import preserve_cwd


def test_preserve_cwd(tmpdir):
    os.chdir(tmpdir)
    directory_before = os.getcwd()
    tmpdir_some_directory = tmpdir.mkdir("some_directory")

    @preserve_cwd
    def change_directory_to(change_to=None):
        os.chdir(change_to)
        return os.getcwd()

    directory_returned = change_directory_to(tmpdir_some_directory)
    directory_after = os.getcwd()

    assert tmpdir_some_directory == directory_returned
    assert directory_after == directory_before
