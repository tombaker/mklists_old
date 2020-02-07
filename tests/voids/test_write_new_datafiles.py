"""Write name2lines_dict to datafiles as named in the dictionary keys."""

import os
from pathlib import Path
import pytest
from mklists.voids import write_new_datafiles


def test_write_new_datafiles(tmp_path):
    """Write name2lines_dict to designated files."""
    os.chdir(tmp_path)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_new_datafiles(data_dict)
    assert "a.txt" in os.listdir()
    assert Path("a.txt").is_file()
    assert [line for line in Path("a.txt").open()][0] == "Line 1\n"
    assert Path("b.txt").read_text() == "Line 3\nLine 4\n"


def test_write_new_datafiles_contents_unless_zero_length(tmp_path):
    """File is not written if value is an empty list."""
    os.chdir(tmp_path)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": []}
    write_new_datafiles(data_dict)
    with pytest.raises(FileNotFoundError):
        Path("b.txt").read_text()
