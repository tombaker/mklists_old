"""Write initial configuration and rule files.

$ mklists init --newbie
    These are installed as examples:
    * /mklists.yml
    * /.rules
    * /a/.rules
    * /a/calendar.txt
    * /a/todo.txt
    * /logs/.rules
    * /logs/log.txt
"""

import io
import os
import yaml
from .constants import (
    CONFIG_YAMLFILE_NAME,
    RULE_YAMLFILE_NAME,
    MINIMAL_CONFIG_YAMLFILE_STR,
    MINIMAL_ADIR_RULES_YAMLFILE_STR,
    NEWBIE_ADIR_RULES_YAMLSTR,
    NEWBIE_BDIR_RULES_YAMLSTR,
    NEWBIE_ROOTDIR_RULES_YAMLSTR,
)


def load_config_yamlfile(mklists_config_yamlfile=CONFIG_YAMLFILE_NAME):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_load_config_yamlfile
    return_pyobj_from_config_yamlfile(mklists_config_yamlfile)
    """
    yaml.load(open(mklists_config_yamlfile).read())


def write_newbie_datafiles():
    """Write newbie data."""


def write_newbie_rule_yamlfiles(
    rulefile=RULE_YAMLFILE_NAME,
    newbie_rootdir_rules=NEWBIE_ROOTDIR_RULES_YAMLSTR,
    newbie_datadira_rules=NEWBIE_ADIR_RULES_YAMLSTR,
    newbie_datadirb_rules=NEWBIE_BDIR_RULES_YAMLSTR,
):
    """Write initial YAML rule files:
    * global rule file (/.rules)
    * folder rule file (/a/.rules)"""
    config_path = os.path.join(os.getcwd())
    grule_file = os.path.join(config_path, rulefile)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", rulefile)
    ruleb_file = os.path.join(config_path, "b", rulefile)
    io.open(grule_file, "w", encoding="utf-8").write(newbie_rootdir_rules)
    io.open(rulea_file, "w", encoding="utf-8").write(newbie_datadira_rules)
    io.open(ruleb_file, "w", encoding="utf-8").write(newbie_datadirb_rules)


def write_initial_config_yamlfile(
    file_written_name=CONFIG_YAMLFILE_NAME,
    file_written_string=MINIMAL_CONFIG_YAMLFILE_STR,
):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile
    Write initial YAML config file ('/mklists.yml')."""
    io.open(file_written_name, "w", encoding="utf-8").write(file_written_string)


def write_initial_rule_yamlfiles():
    """
    MINIMAL_ADIR_RULES_YAMLFILE_STR

    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_initial_rule_yamlfiles
    """
