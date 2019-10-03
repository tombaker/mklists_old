"""Utilities used by other modules."""

import os
import glob
import re
import ruamel.yaml
from .booleans import filename_is_valid_as_filename
from .config import Constants
from .decorators import preserve_cwd
from .exceptions import (
    BadRegexError,
    BadYamlError,
    ConfigFileNotFoundError,
    MissingArgumentError,
    YamlFileNotFoundError,
)

ooo = Constants()


def return_backupdir_pathname(
    _rootdir_pathname=None,
    _backupdir_subdir_name=None,
    _backupdir_shortname=None,
    _timestamp_str=None,
):
    """Generate a timestamped pathname for backups.

    Note: uses output of:
    * return_rootdir_pathname() => here: tmpdir

    Example output:

    Args:
        _rootdir_pathname: Full pathname of mklists repo root directory.
        _backupdir_subdir_name:
        _backupdir_shortname:
        _timestamp_str:
    """
    return os.path.join(
        _rootdir_pathname, _backupdir_subdir_name, _backupdir_shortname, _timestamp_str
    )


def return_backupdir_shortname(_datadir_pathname=None, _rootdir_pathname=None):
    """Creates shortname for backup directory:
    * if directory is on top level, shortname is same as directory name
    * if directory is nested, shortname is chain of directory names separated by underscores

    Note: test for edge case where the following three subdirectories exist:
        .
        ├── a
        │   └── b
        └── a_b

    Problem: "a_b" and "a/b" would both translate into shortname of "a_b" (clash)
    Solutions?
    * Use two underscores instead of one?
    * for each dir in return_datadir_pathnames_under_somedir()
        accumulate a list of shortnames using return_backupdir_shortname(dir) => list comprehension
        accumulate a list of directory names in ".backups"
        compare the two lists and delete unused directories

    See /Users/tbaker/github/tombaker/mklists/tests/test_utils_return_backupdir_shortname_REDO.py
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    return _datadir_pathname[len(_rootdir_pathname) :].strip("/").replace("/", "_")


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


def return_datadir_pathnames_under_somedir(
    _rootdir_pathname=None, _somedir_pathname=None, _rule_yamlfile_name=None
):
    """Return list of data directories under a given directory.

    "Data directories": directories with rules files (by default: '.rules').

    Args:
        _rootdir_pathname: Root of mklists repository.
        _somedir_pathname: Root of data subdirectories.
        _rule_yamlfile_name: Name of rule file.

    2019-07-22: Two scenarios?
    * mklists run         - runs in all data directories in repo
    * mklists run --here  - runs just in current directory
    """
    if not _somedir_pathname:
        _somedir_pathname = os.getcwd()

    datadirs = []
    for dirpath, dirs, files in os.walk(_somedir_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if _rule_yamlfile_name in files:
            datadirs.append(dirpath)

    if _rootdir_pathname in datadirs:
        datadirs.remove(_rootdir_pathname)

    return datadirs


def return_htmldir_pathname(rootdir_pathname, htmldir_name, datadir_name):
    """Return pathname for folder holding htmlified data files.

    Args:
        rootdir_pathname: Full pathname of mklists repo root directory.
        htmldir_name:
        datadir_name:

    Note: uses output of:
    * return_rootdir_pathname() => here: tmpdir

    Example output: '/Users/foobar/github/mylists/.html/a'
    """
    if not rootdir_pathname:
        raise MissingArgumentError(f"Missing argument 'rootdir_pathname'")
    if not htmldir_name:
        raise MissingArgumentError(f"Missing argument 'htmldir_name'")
    if not htmldir_name:
        raise MissingArgumentError(f"Missing argument 'datadir_name'")
    return os.path.join(rootdir_pathname, htmldir_name, datadir_name)


def return_htmlline_from_textline(
    textline=None, url_pattern_regex=ooo.url_pattern_regex
):
    """Return line (ending in \n) with URLs wrapped (with <a href=></a>).

    Args:
        textline: A line of text (a string)."""
    if "<a href=" in textline:
        return textline
    return (
        re.compile(url_pattern_regex).sub(r'<a href="\1">\1</a>', textline.rstrip())
        + "\n"
    )


@preserve_cwd
def return_rootdir_pathname(
    _datadir_pathname=None, config_yamlfile_name=ooo.config_yamlfile_name
):
    """Return repo root pathname when executed anywhere within repo.

    Args:
        _datadir_pathname:
        config_yamlfile_name:
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    while config_yamlfile_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    return os.getcwd()


@preserve_cwd
def return_visiblefiles_list(_datadir_pathname=None):
    """Return list of names of visible files with valid names.

    See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    os.chdir(_datadir_pathname)
    all_datafile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            filename_is_valid_as_filename(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)


def return_yamlobj_from_yamlstr(yamlstr):
    """Returns YAML object from given YAML string."""
    try:
        return ruamel.yaml.safe_load(yamlstr)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")


def return_yamlstr_from_yamlfile(yamlfile_name):
    """Returns YAML object from given YAML-format file."""
    try:
        return open(yamlfile_name).read()
    except FileNotFoundError:
        raise YamlFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")


def return_yamlstr_from_dataobj(dataobj):
    """Returns YAML string from given YAML object."""
    try:
        return ruamel.yaml.safe_dump(dataobj)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")
