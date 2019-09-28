"""Tests for todo.py"""

import os
import pytest
from mklists.run import move_specified_datafiles_elsewhere


# @pytest.mark.skip(reason="todo")
def test_move_specified_datafiles_elsewhere(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    rootdir_pathname = tmpdir
    tmpdir_agendaadir = tmpdir.mkdir("agendaa")
    tmpdir_agendaadir.join("agendab.txt").write("some content")
    tmpdir_agendabdir = tmpdir.mkdir("agendab")
    tmpdir_agendabdir.join("agendaa.txt").write("some content")
    filenames2dirnames_dict = {"agendaa.txt": "agendaa", "agendab.txt": "agendab"}
    move_specified_datafiles_elsewhere(
        _filenames2dirnames_dict=filenames2dirnames_dict,
        _rootdir_pathname=rootdir_pathname,
    )
    assert False
