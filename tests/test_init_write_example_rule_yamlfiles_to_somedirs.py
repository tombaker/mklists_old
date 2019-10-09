"""Docstring"""

import io
import os
import pytest
from mklists.config import Defaults, Samples
from mklists.initialize import write_example_rule_yamlfiles_to_somedirs

fixed = Defaults()


def test_init_write_example_rule_yamlfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, fixed.rule_yamlfile_name)
    assert io.open(rulefile).read() == Samples.rootdir_rules_yamlfile_str


def test_initialize_config_yamlfiles_rulea(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "a", fixed.rule_yamlfile_name)
    assert io.open(rulefile).read() == Samples.example_datadira_rules_yamlfile_str


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "b", fixed.rule_yamlfile_name)
    assert io.open(rulefile).read() == Samples.example_datadirb_rules_yamlfile_str
