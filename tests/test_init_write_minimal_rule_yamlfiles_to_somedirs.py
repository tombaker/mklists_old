"""Tests for todo.py"""

import io
import os
import pytest
from mklists.config import Defaults, Samples
from mklists.initialize import write_minimal_rule_yamlfiles_to_somedirs

fixed = Defaults()


def test_init_write_minimal_rule_yamlfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_rule_yamlfiles_to_somedirs(
        _datadira_file_tobewritten_str=Samples.minimal_datadira_rules_yamlfile_str,
        _datadira_name=Samples.datadira_name,
        _file_tobewritten_name=fixed.rule_yamlfile_name,
        _rootdir_file_tobewritten_str=Samples.rootdir_rules_yamlfile_str,
    )
    assert (
        io.open(
            os.path.join(tmpdir, Samples.datadira_name, fixed.rule_yamlfile_name)
        ).read()
        == Samples.minimal_datadira_rules_yamlfile_str
    )
    assert (
        io.open(os.path.join(tmpdir, fixed.rule_yamlfile_name)).read()
        == Samples.rootdir_rules_yamlfile_str
    )
