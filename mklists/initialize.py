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

# @@@@ Settings x 1, Defaults x 2, Samples x 3
from .config import Defaults, Settings, Samples
from .decorators import preserve_cwd
from .utils import return_rootdir_pathname


def write_config_yamlfile_from_settingsobj_to_rootdir(rootdir_pathname=os.getcwd()):
    """Write initial YAML config file, 'mklists.yml', to root directory."""
    config_yamlfile_name = Defaults.config_yamlfile_name
    contents_tobewritten_dict = attr.asdict(Settings())
    file_tobewritten_name = os.path.join(rootdir_pathname, config_yamlfile_name)
    with open(file_tobewritten_name, "w", encoding="utf-8") as outfile:
        ruamel.yaml.safe_dump(
            contents_tobewritten_dict, outfile, default_flow_style=False
        )


def write_example_datafiles_to_somedirs(
    _datadira_name=None,
    _datadirb_name=None,
    _example_datadira_textfile_name=None,
    _example_datadira_textfile_str=None,
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


def write_example_rule_yamlfiles_to_somedirs(
    rule_yamlfile_name=Defaults.rule_yamlfile_name,
    rootdir_rules_yamlfile_str=Samples.rootdir_rules_yamlfile_str,
    example_datadira_rules_yamlfile_str=Samples.example_datadira_rules_yamlfile_str,
    example_datadirb_rules_yamlfile_str=Samples.example_datadirb_rules_yamlfile_str,
):
    """Write initial YAML rule files:
    * global rule file (/.rules)
    * folder rule file (/a/.rules)"""
    config_path = os.path.join(os.getcwd())
    grule_file = os.path.join(config_path, rule_yamlfile_name)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", rule_yamlfile_name)
    ruleb_file = os.path.join(config_path, "b", rule_yamlfile_name)
    io.open(grule_file, "w", encoding="utf-8").write(rootdir_rules_yamlfile_str)
    io.open(rulea_file, "w", encoding="utf-8").write(
        example_datadira_rules_yamlfile_str
    )
    io.open(ruleb_file, "w", encoding="utf-8").write(
        example_datadirb_rules_yamlfile_str
    )


@preserve_cwd
def write_minimal_rule_yamlfiles_to_somedirs(
    _datadira_name=None,
    _file_tobewritten_name=None,
    _rootdir_file_tobewritten_str=None,
    _datadira_file_tobewritten_str=None,
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
