"""Tests for todo.py"""

import os
import shutil
import pytest
from mklists.run import move_specified_datafiles_elsewhere


@pytest.mark.now
def test_move_specified_datafiles_elsewhere(tmpdir):
    """@@@Docstring"""
    tmpdir_agendaadir = tmpdir.mkdir("agendaa")
    tmpdir_agendaadir.join("agendab.txt").write("some content")
    tmpdir_agendabdir = tmpdir.mkdir("agendab")
    tmpdir_agendabdir.join("agendaa.txt").write("some content")
    filenames2dirnames_dict = {"agendaa.txt": "agendaa", "agendab.txt": "agendab"}
    rootdir_pathname = tmpdir
    assert filenames2dirnames_dict["agendaa.txt"] == "agendaa"
    assert "agendab.txt" in os.listdir(tmpdir_agendaadir)
    os.chdir(tmpdir_agendaadir)
    move_specified_datafiles_elsewhere(
        _filenames2dirnames_dict=filenames2dirnames_dict,
        _rootdir_pathname=rootdir_pathname,
    )
    os.chdir(tmpdir_agendabdir)
    assert "agendab.txt" in os.listdir(tmpdir_agendabdir)
