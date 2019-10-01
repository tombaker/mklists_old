"""@@@Docstring"""

import io
import os
import pytest
from mklists.constants import (
    EXAMPLE_DATADIRA_TEXTFILE_NAME,
    EXAMPLE_DATADIRA_TEXTFILE_STR,
    DATADIRA_NAME,
    DATADIRB_NAME,
)
from mklists.initialize import write_example_datafiles_to_somedirs


def test_write_example_datafiles_to_somedirs(tmpdir):
    """Writes default data files in Folders A and B."""
    os.chdir(tmpdir)
    write_example_datafiles_to_somedirs(
        _example_datadira_textfile_str=EXAMPLE_DATADIRA_TEXTFILE_STR,
        _example_datadira_textfile_name=EXAMPLE_DATADIRA_TEXTFILE_NAME,
        _datadira_name=DATADIRA_NAME,
        _datadirb_name=DATADIRB_NAME,
    )
    datadira_file_pathname = os.path.join(
        tmpdir, DATADIRA_NAME, EXAMPLE_DATADIRA_TEXTFILE_NAME
    )
    assert io.open(datadira_file_pathname).read() == EXAMPLE_DATADIRA_TEXTFILE_STR
