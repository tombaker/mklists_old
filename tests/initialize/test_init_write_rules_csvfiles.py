"""Tests for todo.py"""

import io
import os
import pytest
from mklists.constants import (
    RULES_CSVFILE_NAME,
    DATADIRA_RULES_CSVFILE_CONTENTS,
    DATADIRA_NAME,
    ROOTDIR_RULES_CSVFILE_CONTENTS,
)
from mklists.initialize import write_rules_csvfiles


def test_init_write_rules_csvfiles(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_rules_csvfiles()
    rules_csvfile_name = RULES_CSVFILE_NAME
    datadira_name = DATADIRA_NAME
    rules_csvfile_name = RULES_CSVFILE_NAME
    rootdir_rules_csvfile_contents = ROOTDIR_RULES_CSVFILE_CONTENTS
    datadira_rules_csvfile_contents = DATADIRA_RULES_CSVFILE_CONTENTS
    assert (
        io.open(os.path.join(tmpdir, rules_csvfile_name)).read()
        == rootdir_rules_csvfile_contents
    )
    assert (
        io.open(os.path.join(tmpdir, datadira_name, rules_csvfile_name)).read()
        == datadira_rules_csvfile_contents
    )
