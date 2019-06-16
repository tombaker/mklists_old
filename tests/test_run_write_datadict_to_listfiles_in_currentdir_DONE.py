"""@@@"""

import io
import os
from mklists.run import write_datadict_to_listfiles_in_currentdir


def test_write_datadict_to_listfiles_in_currentdir(tmpdir):
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datadict_to_listfiles_in_currentdir(data_dict)
    assert "a.txt" in os.listdir()


def test_write_datadict_to_listfiles_in_currentdir_contents(tmpdir):
    os.chdir(tmpdir)
    data_dict = {"a.txt": ["Line 1\n", "Line 2\n"], "b.txt": ["Line 3\n", "Line 4\n"]}
    write_datadict_to_listfiles_in_currentdir(data_dict)
    assert io.open("a.txt").read() == "Line 1\nLine 2\n"
