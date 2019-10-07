"""@@@Docstring"""

import io
import os
import pytest
from mklists.config import Samples
from mklists.initialize import write_example_datafiles_to_somedirs


def test_write_example_datafiles_to_somedirs(tmpdir):
    """Writes default data files in Folders A and B."""
    os.chdir(tmpdir)
    write_example_datafiles_to_somedirs(
        _example_datadira_textfile_str=Samples.example_datadira_textfile_str,
        _example_datadira_textfile_name=Samples.example_datadira_textfile_name,
        _datadira_name=Samples.datadira_name,
        _datadirb_name=Samples.datadirb_name,
    )
    datadira_file_pathname = os.path.join(
        tmpdir, Samples.datadira_name, Samples.example_datadira_textfile_name
    )
    assert (
        io.open(datadira_file_pathname).read() == Samples.example_datadira_textfile_str
    )
