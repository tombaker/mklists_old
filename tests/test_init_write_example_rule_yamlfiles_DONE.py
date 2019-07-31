"""Docstring"""

import io
import os
from mklists.initialize import (
    NEWBIE_ROOTDIR_RULE_YAMLSTR,
    NEWBIE_ADIR_RULE_YAMLSTR,
    NEWBIE_BDIR_RULE_YAMLSTR,
    RULE_YAMLFILE_NAME,
    write_example_rule_yamlfiles,
)


def test_init_write_initial_rule_yamlfiles(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_ROOTDIR_RULE_YAMLSTR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_ADIR_RULE_YAMLSTR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == NEWBIE_BDIR_RULE_YAMLSTR
