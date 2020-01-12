"""Docstring"""

import io
import os
import pytest
from mklists.config import Defaults, Samples
from mklists.initialize import write_example_rule_csvfiles_to_somedirs

fixed = Defaults()


def test_init_write_example_rule_csvfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, fixed.rule_csvfile_name)
    assert io.open(rulefile).read() == Samples.rootdir_rules_csvstr


def test_initialize_config_yamlfiles_rulea(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "a", fixed.rule_csvfile_name)
    assert io.open(rulefile).read() == Samples.example_datadira_rules_csvstr


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "b", fixed.rule_csvfile_name)
    assert io.open(rulefile).read() == Samples.example_datadirb_rules_csvstr
