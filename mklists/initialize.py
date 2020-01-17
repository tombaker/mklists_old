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
import attr
import ruamel.yaml

from .constants import (
    CONFIG_YAMLFILE_CONTENT,
    CONFIG_YAMLFILE_NAME,
    DATADIRA_NAME,
    DATADIRA_RULES_CSVFILE_CONTENTS,
    ROOTDIR_RULES_CSVFILE_CONTENTS,
    RULES_CSVFILE_NAME,
)
from .decorators import preserve_cwd
from .utils import return_rootdir_pathname

# pylint: disable=bad-continuation
# Black disagrees.


def write_config_yamlfile_to_rootdir(
    rootdir_pathname=None, config_yamlfile_name=None, config_yamlfile_content=None
):
    """Write initial YAML config file, 'mklists.yml', to root directory."""
    if not rootdir_pathname:
        rootdir_pathname = os.getcwd()
    if not config_yamlfile_name:
        config_yamlfile_name = CONFIG_YAMLFILE_NAME
    if not config_yamlfile_content:
        config_yamlfile_content = CONFIG_YAMLFILE_CONTENT
    file_tobewritten_pathname = os.path.join(rootdir_pathname, config_yamlfile_name)
    with open(file_tobewritten_pathname, "w", encoding="utf-8") as outfile:
        outfile.write(config_yamlfile_content)


@preserve_cwd
def write_rules_csvfiles(
    rules_csvfile_name=None,
    datadira_rules_csvfile_contents=None,
    datadira_name=None,
    rootdir_rules_csvfile_contents=None,
):
    """@@@Docstring"""
    if not rules_csvfile_name:
        rules_csvfile_name = RULES_CSVFILE_NAME
    if not datadira_rules_csvfile_contents:
        datadira_rules_csvfile_contents = DATADIRA_RULES_CSVFILE_CONTENTS
    if not datadira_name:
        datadira_name = DATADIRA_NAME
    if not rootdir_rules_csvfile_contents:
        rootdir_rules_csvfile_contents = ROOTDIR_RULES_CSVFILE_CONTENTS
    io.open(rules_csvfile_name, "w", encoding="utf-8").write(
        rootdir_rules_csvfile_contents
    )
    os.mkdir(datadira_name)
    os.chdir(datadira_name)
    io.open(rules_csvfile_name, "w", encoding="utf-8").write(
        datadira_rules_csvfile_contents
    )
