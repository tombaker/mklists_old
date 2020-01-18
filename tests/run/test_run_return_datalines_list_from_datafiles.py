"""read_datafiles_return_datalines_list()
* takes a list of files
* returns a list of datalines"""

import os
import pytest
from mklists.run import read_datafiles_return_datalines_list


def test_get_lines(tmpdir):
    """Return list of lines aggregated from all data files."""
    os.chdir(tmpdir)
    tmpdir.join("bar").write("bar stuff\nmore bar stuff\n")
    tmpdir.join("foo").write("foo stuff\nmore foo stuff\n")
    expected_result = [
        "bar stuff\n",
        "more bar stuff\n",
        "foo stuff\n",
        "more foo stuff\n",
    ]
    assert read_datafiles_return_datalines_list() == expected_result


def test_get_lines_blank_lines_found(tmpdir):
    """Exit with error message after blank line found."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff\n\n")
    tmpdir.join("bar").write("bar stuff\nmore bar stuff\n")
    with pytest.raises(SystemExit):
        read_datafiles_return_datalines_list()


def test_get_lines_non_utf8_found(tmpdir):
    """Exit with error message after non-UTF8 material found.
    Todo: find out how to write non-UTF8 to a file."""
    import pickle

    os.chdir(tmpdir)
    tmpdir.join("foo").write("foo stuff\nmore foo stuff\n")
    barfile = tmpdir.join("bar.pickle")
    some_data = [{"a": "A", "b": 2, "c": 3.0}]
    with open(barfile, "wb") as fout:
        pickle.dump(some_data, fout)
    with pytest.raises(SystemExit):
        read_datafiles_return_datalines_list()


def test_get_lines_no_data_error(tmpdir):
    """Exit with error message after blank line found."""
    os.chdir(tmpdir)
    tmpdir.join("foo").write("")
    tmpdir.join("bar").write("")
    with pytest.raises(SystemExit):
        read_datafiles_return_datalines_list()
