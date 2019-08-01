"""@@@"""

import io
import os
from mklists.run import write_datafiles_from_datadict


def test_write_datafiles_from_datadict(tmpdir):
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datafiles_from_datadict(data_dict)
    assert "a.txt" in os.listdir()


def test_write_datafiles_from_datadict_contents(tmpdir):
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datafiles_from_datadict(data_dict)
    assert io.open("a.txt").read() == "Line 1\nLine 2\n"
