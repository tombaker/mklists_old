"""Docstring"""

import io
import os
from mklists.constants import (
    NEWBIE_ROOTDIR_RULES_YAMLSTR,
    NEWBIE_DATADIRA_RULES_YAMLSTR,
    NEWBIE_DATADIRB_RULES_YAMLSTR,
    RULE_YAMLFILE_NAME,
)
from mklists.initialize import write_newbie_rule_yamlfiles


def test_init_write_newbie_rule_yamlfiles(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_ROOTDIR_RULES_YAMLSTR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_DATADIRA_RULES_YAMLSTR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_DATADIRB_RULES_YAMLSTR
