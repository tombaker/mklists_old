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
    CONFIG_YAMLFILE_STR,
    DATADIRA_NAME,
    EXAMPLE_DATADIRA_RULES_YAMLFILE_STR,
    EXAMPLE_DATADIRB_RULES_YAMLFILE_STR,
    MINIMAL_DATADIRA_RULES_YAMLFILE_STR,
    ROOTDIR_RULES_YAMLFILE_STR,
    RULE_YAMLFILE_NAME,
)
from .decorators import preserve_cwd


def write_config_yamlfile(
    _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
    _file_tobewritten_str=CONFIG_YAMLFILE_STR,
):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_write_config_yamlfile
    Write initial YAML config file ('/mklists.yml')."""
    io.open(_file_tobewritten_name, "w", encoding="utf-8").write(_file_tobewritten_str)


@preserve_cwd
def write_minimal_rule_yamlfiles(
    _datadira_name=DATADIRA_NAME,
    _file_tobewritten_name=RULE_YAMLFILE_NAME,
    _rootdir_file_tobewritten_str=ROOTDIR_RULES_YAMLFILE_STR,
    _datadira_file_tobewritten_str=MINIMAL_DATADIRA_RULES_YAMLFILE_STR,
):
    """@@@Docstring"""
    io.open(_file_tobewritten_name, "w", encoding="utf-8").write(
        _rootdir_file_tobewritten_str
    )
    os.mkdir(_datadira_name)
    os.chdir(_datadira_name)
    io.open(_file_tobewritten_name, "w", encoding="utf-8").write(
        _datadira_file_tobewritten_str
    )


def write_newbie_datafiles():
    """Write newbie data."""


def write_newbie_rule_yamlfiles(
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    _newbie_rootdir_rules_yamlfile_str=ROOTDIR_RULES_YAMLFILE_STR,
    _newbie_datadira_rules_yamlfile_str=EXAMPLE_DATADIRA_RULES_YAMLFILE_STR,
    _newbie_datadirb_rules_yamlfile_str=EXAMPLE_DATADIRB_RULES_YAMLFILE_STR,
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
    io.open(grule_file, "w", encoding="utf-8").write(_newbie_rootdir_rules_yamlfile_str)
    io.open(rulea_file, "w", encoding="utf-8").write(
        _newbie_datadira_rules_yamlfile_str
    )
    io.open(ruleb_file, "w", encoding="utf-8").write(
        _newbie_datadirb_rules_yamlfile_str
    )
