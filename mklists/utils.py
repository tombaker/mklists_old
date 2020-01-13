"""Utilities used by other modules."""

import csv
import os
import glob
import re
import ruamel.yaml
from .booleans import filename_is_valid_as_filename

from .config import URL_PATTERN_REGEX, RULES_CSVFILE_NAME, ROOTDIR_PATHNAME
from .decorators import preserve_cwd
from .exceptions import (
    BadRegexError,
    BadYamlError,
    BlankLinesError,
    ConfigFileNotFoundError,
    MissingArgumentError,
    NoDataError,
    NotUTF8Error,
    YamlFileNotFoundError,
)

# pylint: disable=bad-continuation
# Black disagrees.


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


def return_datadir_pathnames_under_given_pathname(given_pathname=os.getcwd()):
    """Return list of data directories under a given directory.

    "Data directories": directories with rules files (by default: '.rules').

    Args:
        given_pathname: starting point for finding data subdirectories.

    2019-07-22: Two scenarios?
    * mklists run         - runs in all data directories in repo
    * mklists run --here  - runs just in current directory
    """
    datadirs = []
    for dirpath, dirs, files in os.walk(given_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if RULES_CSVFILE_NAME in files:
            datadirs.append(dirpath)

    if ROOTDIR_PATHNAME in datadirs:
        datadirs.remove(ROOTDIR_PATHNAME)

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


def return_pyobj_from_yamlstr(yamlstr):
    """Returns YAML object from given YAML string."""
    try:
        return ruamel.yaml.safe_load(yamlstr)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")


def return_yamlstr_from_pyobj(pyobj):
    """Returns YAML string from given Python object."""
    try:
        return ruamel.yaml.safe_dump(pyobj)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")
