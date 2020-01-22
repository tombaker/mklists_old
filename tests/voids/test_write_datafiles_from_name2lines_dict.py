"""@@@"""

import io
import os
import pytest
from mklists.voids import write_datafiles_from_name2lines_dict


def test_write_datafiles_from_name2lines_dict(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datafiles_from_name2lines_dict(data_dict)
    assert "a.txt" in os.listdir()


def test_write_datafiles_from_name2lines_dict_contents(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datafiles_from_name2lines_dict(data_dict)
    assert io.open("a.txt").read() == "Line 1\nLine 2\n"


@pytest.mark.improve
def test_write_datafiles_from_name2lines_dict_contents_unless_zero_length(tmpdir):
    """Does not write file if value is empty list.

    2019-09-28: Unclear if this is needed."""
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": []}
    write_datafiles_from_name2lines_dict(data_dict)
    with pytest.raises(FileNotFoundError):
        io.open("b.txt")
