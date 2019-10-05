"""@@@Docstring"""

import io
import os
import pytest
from mklists.config import Examples
from mklists.initialize import write_example_datafiles_to_somedirs


def test_write_example_datafiles_to_somedirs(tmpdir):
    """Writes default data files in Folders A and B."""
    os.chdir(tmpdir)
    write_example_datafiles_to_somedirs(
        _example_datadira_textfile_str=Examples.example_datadira_textfile_str,
        _example_datadira_textfile_name=Examples.example_datadira_textfile_name,
        _datadira_name=Examples.datadira_name,
        _datadirb_name=Examples.datadirb_name,
    )
    datadira_file_pathname = os.path.join(
        tmpdir, Examples.datadira_name, Examples.example_datadira_textfile_name
    )
    assert (
        io.open(datadira_file_pathname).read() == Examples.example_datadira_textfile_str
    )
