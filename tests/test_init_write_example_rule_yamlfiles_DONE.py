"""Docstring"""

import io
import os
from mklists.initialize import (
    INITIAL_EXAMPLE_GLOBALRULE_YAMLFILE_STR,
    INITIAL_EXAMPLE_RULEA_YAMLFILE_STR,
    INITIAL_EXAMPLE_RULEB_YAMLFILE_STR,
    RULE_YAMLFILE_NAME,
    write_example_rule_yamlfiles,
)


def test_init_write_initial_rule_yamlfiles(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == INITIAL_EXAMPLE_GLOBALRULE_YAMLFILE_STR


def test_initialize_config_yamlfiles_rulea(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == INITIAL_EXAMPLE_RULEA_YAMLFILE_STR


def test_initialize_config_yamlfiles_ruleb(tmpdir):
    os.chdir(tmpdir)
    write_example_rule_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == INITIAL_EXAMPLE_RULEB_YAMLFILE_STR
