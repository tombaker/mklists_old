"""@@@"""

import io
import os
from mklists.initialize import initialize_config_yamlfiles
from mklists.constants import (
    CONFIG_YAMLFILE_YAMLSTR,
    CONFIG_YAMLFILE_NAME,
    RULE_YAMLFILE_NAME,
    GRULE_YAMLFILE_STARTER_YAMLSTR,
    RULEA_YAMLFILE_STARTER_YAMLSTR,
    RULEB_YAMLFILE_STARTER_YAMLSTR,
)


def test_utils_initialize_config_yamlfiles_config(tmpdir):
    os.chdir(tmpdir)
    initialize_config_yamlfiles()
    configfile = os.path.join(tmpdir, CONFIG_YAMLFILE_NAME)
    assert io.open(configfile).read() == CONFIG_YAMLFILE_YAMLSTR


def test_utils_initialize_config_yamlfiles_rules(tmpdir):
    os.chdir(tmpdir)
    initialize_config_yamlfiles()
    rulefile = os.path.join(tmpdir, RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == GRULE_YAMLFILE_STARTER_YAMLSTR


def test_utils_initialize_config_yamlfiles_rulea(tmpdir):
    os.chdir(tmpdir)
    initialize_config_yamlfiles()
    rulefile = os.path.join(tmpdir, "a", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == RULEA_YAMLFILE_STARTER_YAMLSTR


def test_utils_initialize_config_yamlfiles_ruleb(tmpdir):
    os.chdir(tmpdir)
    initialize_config_yamlfiles()
    rulefile = os.path.join(tmpdir, "b", RULE_YAMLFILE_NAME)
    assert io.open(rulefile).read() == RULEB_YAMLFILE_STARTER_YAMLSTR
