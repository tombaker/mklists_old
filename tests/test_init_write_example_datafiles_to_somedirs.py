"""@@@Docstring"""

import io
import os
import pytest
from mklists.config import ex
from mklists.initialize import write_example_datafiles_to_somedirs


def test_write_example_datafiles_to_somedirs(tmpdir):
    """Writes default data files in Folders A and B."""
    os.chdir(tmpdir)
    write_example_datafiles_to_somedirs(
        _example_datadira_textfile_str=ex.example_datadira_textfile_str,
        _example_datadira_textfile_name=ex.example_datadira_textfile_name,
        _datadira_name=ex.datadira_name,
        _datadirb_name=ex.datadirb_name,
    )
    datadira_file_pathname = os.path.join(
        tmpdir, ex.datadira_name, ex.example_datadira_textfile_name
    )
    assert io.open(datadira_file_pathname).read() == ex.example_datadira_textfile_str
