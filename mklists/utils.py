"""Utilities used by other modules."""

import csv
import os
import glob
import re
import ruamel.yaml
from .booleans import filename_is_valid_as_filename

from .constants import (
    BACKUPS_DIR_NAME,
    CONFIG_YAMLFILE_NAME,
    RULES_CSVFILE_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
)
from .decorators import preserve_cwd
from .exceptions import (
    BadRegexError,
    BadYamlError,
    BlankLinesError,
    ConfigFileNotFoundError,
    MissingArgumentError,
    NoDataError,
    NotUTF8Error,
)

# pylint: disable=bad-continuation
# Black disagrees.


def return_config_dict_from_config_yamlfile(
    rootdir_pathname=None, config_yamlfile_name=None
):
    """Returns configuration dictionary from YAML config file."""
    if rootdir_pathname:
        os.chdir(rootdir_pathname)
    if not config_yamlfile_name:
        config_yamlfile_name = CONFIG_YAMLFILE_NAME
    try:
        config_yamlfile_contents = open(config_yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(
            f"Config file {repr(config_yamlfile_name)} not found."
        )
    try:
        return ruamel.yaml.safe_load(config_yamlfile_contents)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")


@preserve_cwd
def return_rootdir_pathname(startdir_pathname=None):
    """Return root pathname of mklists repo wherever executed in repo."""
    if not startdir_pathname:
        startdir_pathname = os.getcwd()
    while "mklists.yml" not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            return None
    return os.getcwd()


@preserve_cwd
def return_backup_subdir_name(rootdir_pathname=None, datadir_pathname=None):
    """@@@Docstring"""
    if not datadir_pathname:
        datadir_pathname = os.getcwd()
    if not rootdir_pathname:
        rootdir_pathname = return_rootdir_pathname(startdir_pathname=datadir_pathname)
    if rootdir_pathname == datadir_pathname:
        return "rootdir"
    return datadir_pathname[len(rootdir_pathname) :].strip("/").replace("/", "_")


@preserve_cwd
def return_backupdir_pathname(
    rootdir_pathname=None,
    backups_dir_name=None,
    backup_subdir_name=None,
    timestamp_str=None,
):
    """@@@Docstring"""
    rootdir_pathname = return_rootdir_pathname()
    backups_dir_name = BACKUPS_DIR_NAME
    backup_subdir_name = return_backup_subdir_name()
    timestamp_str = TIMESTAMP_STR
    return os.path.join(
        rootdir_pathname, backups_dir_name, backup_subdir_name, timestamp_str
    )


def return_compiled_regex_from_regexstr(_regex=None):
    """Return compiled regex from regular expression.

    Args:
        _regex: a regular expression

    Raises:
        BadRegexError: string does not compile as regular expression
    """
    try:
        compiled_regex = re.compile(_regex)
    except re.error:
        raise BadRegexError(
            f"{repr(_regex)} does not correctly compile as Python regex"
        )
    return compiled_regex


def return_datadir_pathnames_under_given_pathname(given_pathname=None):
    """Return list of data directories under a given directory.

    "Data directories"
    * directories with a rule file (default: RULES_CSVFILE_NAME = '.rules')
      * repo root directory (ROOTDIR_PATHNAME) may have rule file
        but is not a data directory
      * except "hidden" directories (name starting with ".")

    Args:
        given_pathname: starting point for finding data subdirectories.

    2019-07-22: Two scenarios?
    * mklists run --all   - runs in all data directories under repo root directory
    * mklists run         - runs in all data directories under current directory
    * mklists run --here  - runs just in current directory
    """
    if not given_pathname:
        given_pathname = os.getcwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(given_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if RULES_CSVFILE_NAME in files:
            if CONFIG_YAMLFILE_NAME not in files:
                datadirs.append(dirpath)

    return datadirs


def return_htmldir_pathname(rootdir_pathname, htmldir_name, datadir_name):
    """Return pathname for folder holding htmlified data files.

    Args:
        rootdir_pathname: Full pathname of mklists repo root directory.
        htmldir_name:
        datadir_name:
    """
    if not rootdir_pathname:
        raise MissingArgumentError(f"Missing argument 'rootdir_pathname'")
    if not htmldir_name:
        raise MissingArgumentError(f"Missing argument 'htmldir_name'")
    if not htmldir_name:
        raise MissingArgumentError(f"Missing argument 'datadir_name'")
    return os.path.join(rootdir_pathname, htmldir_name, datadir_name)


def return_htmlline_from_textline(textline=None, url_pattern_regex=URL_PATTERN_REGEX):
    """Return line (ending in \n) with URLs wrapped (with <a href=></a>).

    Args:
        textline: A line of text (a string)."""
    if "<a href=" in textline:
        return textline
    return (
        re.compile(url_pattern_regex).sub(r'<a href="\1">\1</a>', textline.rstrip())
        + "\n"
    )


def return_visiblefiles_list():
    """Return list of names of visible files with valid names.

    See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
    """
    all_datafile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            filename_is_valid_as_filename(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)
