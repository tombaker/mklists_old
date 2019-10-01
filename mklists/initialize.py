"""Write initial configuration and rule files.

$ mklists init --example-data
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
    DATADIRB_NAME,
    EXAMPLE_DATADIRA_RULES_YAMLFILE_STR,
    EXAMPLE_DATADIRA_TEXTFILE_STR,
    EXAMPLE_DATADIRA_TEXTFILE_NAME,
    EXAMPLE_DATADIRB_RULES_YAMLFILE_STR,
    MINIMAL_DATADIRA_RULES_YAMLFILE_STR,
    ROOTDIR_RULES_YAMLFILE_STR,
    RULE_YAMLFILE_NAME,
)
from .decorators import preserve_cwd


def write_config_yamlfile_to_rootdir(
    _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
    _file_tobewritten_str=CONFIG_YAMLFILE_STR,
):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_write_config_yamlfile_to_rootdir
    Write initial YAML config file ('/mklists.yml')."""
    io.open(_file_tobewritten_name, "w", encoding="utf-8").write(_file_tobewritten_str)


def write_example_datafiles_to_somedirs(
    _datadira_name=DATADIRA_NAME,
    _datadirb_name=DATADIRB_NAME,
    _example_datadira_textfile_name=EXAMPLE_DATADIRA_TEXTFILE_NAME,
    _example_datadira_textfile_str=EXAMPLE_DATADIRA_TEXTFILE_STR,
):
    """Writes example data files (plain-text lists) to Folders A and B.

    Creates folders A and B.

    Args:
        _datadira_name: Name of data file to be written in Folder A.
        _datadirb_name: Name of data file to be written in Folder B.
        _example_datadira_textfile_name: Name of file to be written in Folder A.
        _example_datadira_textfile_str: Content to be written to data file in Folder A.
    """
    cwd_pathname = os.path.join(os.getcwd())
    os.makedirs(os.path.join(cwd_pathname, _datadira_name))
    os.makedirs(os.path.join(cwd_pathname, _datadirb_name))
    datadira_file_name = os.path.join(
        cwd_pathname, _datadira_name, _example_datadira_textfile_name
    )
    io.open(datadira_file_name, "w", encoding="utf-8").write(
        _example_datadira_textfile_str
    )


def write_example_rule_yamlfiles(
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    _rootdir_rules_yamlfile_str=ROOTDIR_RULES_YAMLFILE_STR,
    _example_datadira_rules_yamlfile_str=EXAMPLE_DATADIRA_RULES_YAMLFILE_STR,
    _example_datadirb_rules_yamlfile_str=EXAMPLE_DATADIRB_RULES_YAMLFILE_STR,
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
    io.open(grule_file, "w", encoding="utf-8").write(_rootdir_rules_yamlfile_str)
    io.open(rulea_file, "w", encoding="utf-8").write(
        _example_datadira_rules_yamlfile_str
    )
    io.open(ruleb_file, "w", encoding="utf-8").write(
        _example_datadirb_rules_yamlfile_str
    )


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
