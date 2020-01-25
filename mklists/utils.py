"""Utilities used by other modules."""

import os
import glob
import re
from pathlib import Path
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


def return_datalines_list_from_datafiles():
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
                print("Files in data directory must contain no blank lines.")
                raise BlankLinesError(f"{repr(datafile)} has blank lines.")
        all_datalines.extend(datafile_lines)

    if not all_datalines:
        raise NoDataError("No data to process!")
    return all_datalines


def return_config_dict_from_config_yamlfile(
    rootdir_pathname=None, config_yamlfile_name=CONFIG_YAMLFILE_NAME
):
    """Returns configuration dictionary from YAML config file."""
    if rootdir_pathname:
        os.chdir(rootdir_pathname)
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
def return_rootdir_pathname(here=None, configfile=CONFIG_YAMLFILE_NAME):
    """Return root pathname of mklists repo wherever executed in repo."""
    if not here:
        here = Path.cwd()
    directory_chain_upwards = list(Path(here).parents)
    directory_chain_upwards.insert(0, Path.cwd())
    for directory in directory_chain_upwards:
        if configfile in [item.name for item in directory.glob("*")]:
            return directory
    return None


@preserve_cwd
def return_backup_subdir_name(rootdir=None, heredir=None):
    """Return shortname of backup subdirectory."""
    if not heredir:
        heredir = Path.cwd()
    if not rootdir:
        rootdir = return_rootdir_pathname(here=heredir)
    if rootdir == heredir:
        return "rootdir"
    return str(heredir)[len(str(rootdir)) :].strip("/").replace("/", "_")


@preserve_cwd
def return_backupdir_pathname(
    rootdir=None,
    backupsdir=BACKUPS_DIR_NAME,
    backup_subdir=None,
    timestamp=TIMESTAMP_STR,
):
    """@@@Docstring"""
    rootdir = return_rootdir_pathname()
    backup_subdir = return_backup_subdir_name()
    return Path(rootdir) / backupsdir / backup_subdir / timestamp


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


def return_datadir_pathnames_under_given_pathname(
    given_pathname=None,
    config_yamlfile_name=CONFIG_YAMLFILE_NAME,
    rules_csvfile_name=RULES_CSVFILE_NAME,
):
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
        if rules_csvfile_name in files:
            if config_yamlfile_name not in files:
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
