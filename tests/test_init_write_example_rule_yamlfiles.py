"""Docstring"""

import io
import os
from mklists.constants import (
    ROOTDIR_RULES_YAMLFILE_STR,
    EXAMPLE_DATADIRA_RULES_YAMLFILE_STR,
    EXAMPLE_DATADIRB_RULES_YAMLFILE_STR,
    RULE_YAMLFILE_NAME,
)
from mklists.initialize import write_example_rule_yamlfiles


def test_init_write_example_rule_yamlfiles(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == ROOTDIR_RULES_YAMLFILE_STR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == EXAMPLE_DATADIRA_RULES_YAMLFILE_STR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == EXAMPLE_DATADIRB_RULES_YAMLFILE_STR
