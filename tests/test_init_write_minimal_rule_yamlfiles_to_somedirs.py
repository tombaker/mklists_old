"""Tests for todo.py"""

import io
import os
import pytest
from mklists.config import Constants, ConfigExamples
from mklists.initialize import write_minimal_rule_yamlfiles_to_somedirs


def test_init_write_minimal_rule_yamlfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    ooo = Constants()
    xxx = ConfigExamples()
    write_minimal_rule_yamlfiles_to_somedirs(
        _datadira_file_tobewritten_str=xxx.minimal_datadira_rules_yamlfile_str,
        _datadira_name=xxx.datadira_name,
        _file_tobewritten_name=ooo.rule_yamlfile_name,
        _rootdir_file_tobewritten_str=xxx.rootdir_rules_yamlfile_str,
    )
    assert (
        io.open(os.path.join(tmpdir, xxx.datadira_name, ooo.rule_yamlfile_name)).read()
        == xxx.minimal_datadira_rules_yamlfile_str
    )
    assert (
        io.open(os.path.join(tmpdir, ooo.rule_yamlfile_name)).read()
        == xxx.rootdir_rules_yamlfile_str
    )
