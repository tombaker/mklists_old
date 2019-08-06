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
from .constants import (
    CONFIG_YAMLFILE_NAME,
    RULE_YAMLFILE_NAME,
    MINIMAL_CONFIG_YAMLFILE_STR,
    NEWBIE_ADIR_RULES_YAMLSTR,
    NEWBIE_BDIR_RULES_YAMLSTR,
    NEWBIE_ROOTDIR_RULES_YAMLSTR,
)

#     MINIMAL_ADIR_RULES_YAMLFILE_STR,


def write_newbie_config_yamlfile():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_minimal_rule_yamlfiles
    """


def write_newbie_datafiles():
    """Write newbie data."""


def write_newbie_rule_yamlfiles(
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    newbie_rootdir_rules=NEWBIE_ROOTDIR_RULES_YAMLSTR,
    newbie_datadira_rules=NEWBIE_ADIR_RULES_YAMLSTR,
    newbie_datadirb_rules=NEWBIE_BDIR_RULES_YAMLSTR,
):
    """Write initial YAML rule files:
    * global rule file (/.rules)
    * folder rule file (/a/.rules)"""
    config_path = os.path.join(os.getcwd())
    grule_file = os.path.join(config_path, _rule_yamlfile_name)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", _rule_yamlfile_name)
    ruleb_file = os.path.join(config_path, "b", _rule_yamlfile_name)
    io.open(grule_file, "w", encoding="utf-8").write(newbie_rootdir_rules)
    io.open(rulea_file, "w", encoding="utf-8").write(newbie_datadira_rules)
    io.open(ruleb_file, "w", encoding="utf-8").write(newbie_datadirb_rules)


def write_minimal_config_yamlfile(
    _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
    file_written_string=MINIMAL_CONFIG_YAMLFILE_STR,
):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_write_minimal_config_yamlfile
    Write initial YAML config file ('/mklists.yml')."""
    io.open(_file_tobewritten_name, "w", encoding="utf-8").write(file_written_string)


def write_minimal_rule_yamlfiles():
    """
    MINIMAL_ADIR_RULES_YAMLFILE_STR

    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_minimal_rule_yamlfiles
    """
