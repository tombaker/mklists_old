"""Functions that return lists or dictionaries from reading files."""

import ruamel.yaml
from pathlib import Path
from .constants import CONFIGFILE_NAME
from .exceptions import (
    BadYamlError,
    BlankLinesError,
    ConfigFileNotFoundError,
    NoDataError,
    NotUTF8Error,
)
from .utils import return_rootdir_path, return_visiblefiles_list


def read_datafiles():
    """Returns lines from files in current directory.

    Exits with error message if it encounters:
    * file that has an invalid name
    * file that is not UTF8-encoded
    * file that has blank lines."""
    visiblefiles_list = return_visiblefiles_list()
    all_datalines = []
    for datafile in visiblefiles_list:
        try:
            datafile_lines = open(datafile).readlines()
        except UnicodeDecodeError:
            raise NotUTF8Error(f"{repr(datafile)} is not UTF8-encoded.")
        for line in datafile_lines:
            if not line.rstrip():
                raise BlankLinesError(f"{repr(datafile)} must have no blank lines.")
        all_datalines.extend(datafile_lines)
    if not all_datalines:
        raise NoDataError("No data to process!")
    return all_datalines


def read_configfile(rootdir_pathname=None, configfile_name=CONFIGFILE_NAME):
    """Returns configuration dictionary from YAML config file."""
    if not rootdir_pathname:
        rootdir_pathname = return_rootdir_path()
    configfile = Path(rootdir_pathname) / configfile_name
    try:
        configfile_contents = Path(configfile).read_text()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"Config file {repr(configfile)} not found.")
    try:
        return ruamel.yaml.safe_load(configfile_contents)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")
