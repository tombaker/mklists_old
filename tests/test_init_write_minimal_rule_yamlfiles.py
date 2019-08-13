"""Tests for todo.py"""

import io
import os
import pytest
from mklists.constants import (
    DATADIRA_NAME,
    RULE_YAMLFILE_NAME,
    ROOTDIR_RULES_YAMLFILE_STR,
    MINIMAL_DATADIRA_RULES_YAMLFILE_STR,
)
from mklists.initialize import write_minimal_rule_yamlfiles


def test_init_write_minimal_rule_yamlfiles(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_rule_yamlfiles(
        _datadira_file_tobewritten_str=MINIMAL_DATADIRA_RULES_YAMLFILE_STR,
        _datadira_name=DATADIRA_NAME,
        _file_tobewritten_name=RULE_YAMLFILE_NAME,
        _rootdir_file_tobewritten_str=ROOTDIR_RULES_YAMLFILE_STR,
    )
    assert (
        io.open(os.path.join(tmpdir, DATADIRA_NAME, RULE_YAMLFILE_NAME)).read()
        == MINIMAL_DATADIRA_RULES_YAMLFILE_STR
    )
    assert (
        io.open(os.path.join(tmpdir, RULE_YAMLFILE_NAME)).read()
        == ROOTDIR_RULES_YAMLFILE_STR
    )
