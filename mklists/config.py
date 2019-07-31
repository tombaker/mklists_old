"""Functions related to configuration"""

import yaml
from .exceptions import ConfigFileNotFoundError, BadYamlError


def return_pyobj_from_config_yamlfile(yamlfile_name=None):
    """Returns Python object parsed from given YAML-format file."""
    try:
        yamlstr = open(yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")

    try:
        return yaml.load(yamlstr)
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(yamlfile_name)}.")
