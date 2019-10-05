"""Tests for todo.py"""

import io
import os
import pytest
from mklists.config import fixed, ConfigExamples
from mklists.initialize import write_minimal_rule_yamlfiles_to_somedirs


def test_init_write_minimal_rule_yamlfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_rule_yamlfiles_to_somedirs(
        _datadira_file_tobewritten_str=ConfigExamples.minimal_datadira_rules_yamlfile_str,
        _datadira_name=ConfigExamples.datadira_name,
        _file_tobewritten_name=fixed.rule_yamlfile_name,
        _rootdir_file_tobewritten_str=ConfigExamples.rootdir_rules_yamlfile_str,
    )
    assert (
        io.open(
            os.path.join(tmpdir, ConfigExamples.datadira_name, fixed.rule_yamlfile_name)
        ).read()
        == ConfigExamples.minimal_datadira_rules_yamlfile_str
    )
    assert (
        io.open(os.path.join(tmpdir, fixed.rule_yamlfile_name)).read()
        == ConfigExamples.rootdir_rules_yamlfile_str
    )
