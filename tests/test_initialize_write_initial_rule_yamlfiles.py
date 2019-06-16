"""Docstring"""

import io
import os
from mklists.initialize import (
    INITIAL_GLOBALRULE_YAMLFILE_STR,
    RULEA_YAMLFILE_STARTER_YAMLSTR,
    RULEB_YAMLFILE_STARTER_YAMLSTR,
    RULE_YAMLFILE_NAME,
    write_initial_rule_yamlfiles,
)


def test_initialize_write_initial_rule_yamlfiles(tmpdir):
    os.chdir(tmpdir)
    write_initial_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == INITIAL_GLOBALRULE_YAMLFILE_STR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    os.chdir(tmpdir)
    write_initial_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == RULEA_YAMLFILE_STARTER_YAMLSTR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    os.chdir(tmpdir)
    write_initial_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == RULEB_YAMLFILE_STARTER_YAMLSTR
