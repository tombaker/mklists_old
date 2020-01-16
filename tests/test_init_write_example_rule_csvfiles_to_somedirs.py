"""Docstring"""

import io
import os
import pytest
from mklists.constants import Samples, RULES_CSVFILE_NAME
from mklists.initialize import write_example_rules_csvfiles_to_somedirs


def test_init_write_example_rules_csvfiles_to_somedirs(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rules_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, RULES_CSVFILE_NAME)
    assert io.open(rulefile).read() == Samples.rootdir_rules_csvstr


def test_initialize_config_yamlfiles_rulea(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rules_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "a", RULES_CSVFILE_NAME)
    assert io.open(rulefile).read() == Samples.example_datadira_rules_csvstr


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rules_csvfiles_to_somedirs()
    rulefile = os.path.join(tmpdir, "b", RULES_CSVFILE_NAME)
    assert io.open(rulefile).read() == Samples.example_datadirb_rules_csvstr
