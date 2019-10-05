"""Tests for todo.py"""

import io
import os
import pytest
from mklists.config import fixed, ex
from mklists.initialize import write_minimal_rule_yamlfiles_to_somedirs


def test_init_write_minimal_rule_yamlfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_rule_yamlfiles_to_somedirs(
        _datadira_file_tobewritten_str=ex.minimal_datadira_rules_yamlfile_str,
        _datadira_name=ex.datadira_name,
        _file_tobewritten_name=fixed.rule_yamlfile_name,
        _rootdir_file_tobewritten_str=ex.rootdir_rules_yamlfile_str,
    )
    assert (
        io.open(os.path.join(tmpdir, ex.datadira_name, fixed.rule_yamlfile_name)).read()
        == ex.minimal_datadira_rules_yamlfile_str
    )
    assert (
        io.open(os.path.join(tmpdir, fixed.rule_yamlfile_name)).read()
        == ex.rootdir_rules_yamlfile_str
    )
