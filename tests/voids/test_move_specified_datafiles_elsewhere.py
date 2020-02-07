"""Tests for todo.py"""

import os
from mklists.voids import move_specified_datafiles_elsewhere


def test_move_specified_datafiles_elsewhere(tmpdir):
    """Basic test of move_specified_datafiles_elsewhere plus:
    * extra test of filenames2dirnames_dict
    * extra test of file system before move_specified_datafiles_elsewhere run"""
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


def test_move_specified_datafiles_elsewhere_as_subdir(tmpdir):
    """Test of move_specified_datafiles_elsewhere where:
    * file moved to specific subdirectory under repo root directory

    Note that destination directory is defined relative to repo root directory"""
    tmpdir_listsdir = tmpdir.mkdir("lists")
    tmpdir_agendaadir = tmpdir_listsdir.mkdir("agendaa")
    tmpdir_agendaadir.join("agendab.txt").write("some content")
    tmpdir_agendabdir = tmpdir_listsdir.mkdir("agendab")
    tmpdir_agendabdir.join("agendaa.txt").write("some content")
    filenames2dirnames_dict = {
        "agendaa.txt": "lists/agendaa",
        "agendab.txt": "lists/agendab",
    }
    rootdir_pathname = tmpdir
    os.chdir(tmpdir_agendaadir)
    move_specified_datafiles_elsewhere(
        _filenames2dirnames_dict=filenames2dirnames_dict,
        _rootdir_pathname=rootdir_pathname,
    )
    os.chdir(tmpdir_agendabdir)
    assert "agendab.txt" in os.listdir(tmpdir_agendabdir)


def test_move_specified_datafiles_elsewhere_as_external_dir(tmpdir):
    """Test of move_specified_datafiles_elsewhere where:
    * file moved to directory outside of the repo
    * assumes existence of a /tmp directory in filesystem

    Destination directory defined relative to root of filesystem"""
    tmpdir_listsdir = tmpdir.mkdir("lists")
    tmpdir_agendaadir = tmpdir_listsdir.mkdir("agendaa")
    tmpdir_agendaadir.join("agendab.txt").write("some content")
    tmpdir_agendabdir = tmpdir_listsdir.mkdir("agendab")
    tmpdir_agendabdir.join("agendaa.txt").write("some content")
    filenames2dirnames_dict = {"agendaa.txt": "lists/agendaa", "agendab.txt": "/tmp"}
    rootdir_pathname = tmpdir
    if os.path.exists("/tmp/agendab.txt"):  # clean-up, sometimes needed
        os.remove("/tmp/agendab.txt")
    os.chdir(tmpdir_agendaadir)
    move_specified_datafiles_elsewhere(
        _filenames2dirnames_dict=filenames2dirnames_dict,
        _rootdir_pathname=rootdir_pathname,
    )
    os.chdir("/tmp")
    assert "agendab.txt" in os.listdir("/tmp")
