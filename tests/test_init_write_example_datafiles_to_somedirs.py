"""@@@Docstring"""

import io
import os
import pytest
from mklists.config import ConfigExamples
from mklists.initialize import write_example_datafiles_to_somedirs


def test_write_example_datafiles_to_somedirs(tmpdir):
    """Writes default data files in Folders A and B."""
    os.chdir(tmpdir)
    x = ConfigExamples()
    write_example_datafiles_to_somedirs(
        _example_datadira_textfile_str=x.example_datadira_textfile_str,
        _example_datadira_textfile_name=x.example_datadira_textfile_name,
        _datadira_name=x.datadira_name,
        _datadirb_name=x.datadirb_name,
    )
    datadira_file_pathname = os.path.join(
        tmpdir, x.datadira_name, x.example_datadira_textfile_name
    )
    assert io.open(datadira_file_pathname).read() == x.example_datadira_textfile_str
