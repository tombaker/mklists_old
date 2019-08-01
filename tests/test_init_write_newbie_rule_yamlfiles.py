"""Docstring"""

import io
import os
from mklists.constants import (
    NEWBIE_ROOTDIR_RULES_YAMLSTR,
    NEWBIE_ADIR_RULES_YAMLSTR,
    NEWBIE_BDIR_RULES_YAMLSTR,
    RULE_YAMLFILE_NAME,
)
from mklists.initialize import write_newbie_rule_yamlfiles


def test_init_write_newbie_rule_yamlfiles(tmpdir):
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_ROOTDIR_RULES_YAMLSTR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_ADIR_RULES_YAMLSTR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    os.chdir(tmpdir)
    write_newbie_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_BDIR_RULES_YAMLSTR
