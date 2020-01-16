"""Tests for todo.py"""

import io
import os
import pytest
from mklists.constants import Samples, RULES_CSVFILE_NAME
from mklists.initialize import write_minimal_rules_csvfiles_to_somedirs


@pytest.mark.skip
def test_init_write_minimal_rules_csvfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_rules_csvfiles_to_somedirs(
        _datadira_file_tobewritten_str=Samples.minimal_datadira_rules_csvstr,
        _datadira_name=Samples.datadira_name,
        _file_tobewritten_name=RULES_CSVFILE_NAME,
        _rootdir_file_tobewritten_str=Samples.rootdir_rules_csvstr,
    )
    assert (
        io.open(os.path.join(tmpdir, Samples.datadira_name, RULES_CSVFILE_NAME)).read()
        == Samples.minimal_datadira_rules_csvstr
    )
    assert (
        io.open(os.path.join(tmpdir, RULES_CSVFILE_NAME)).read()
        == Samples.rootdir_rules_csvstr
    )
