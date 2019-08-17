"""Utilities used by other modules."""

import os
import glob
import re
import ruamel.yaml
from .booleans import is_valid_as_filename
from .constants import (
    CONFIG_YAMLFILE_NAME,
    HTMLDIR_NAME,
    RULE_YAMLFILE_NAME,
    URL_PATTERN_REGEX,
)
from .decorators import preserve_cwd
from .exceptions import (
    BadRegexError,
    BadYamlError,
    ConfigFileNotFoundError,
    MissingArgumentError,
    YamlFileNotFoundError,
)


def return_compiled_regex(_regex=None):
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


def return_htmlstr_from_textstr(_textstr=None):
    """Return string with URLs wrapped with <a href=></a> HTML tags.

    Args:
        _textstr: A text string (typically, one line of text)."""
    if "<a href=" in _textstr:
        return _textstr
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', _textstr)


def return_pyobj_from_yamlstr(_yamlstr=None):
    """Returns YAML object from given YAML-format file."""
    try:
        return ruamel.yaml.safe_load(_yamlstr)
    except ruamel.yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML content.")


@preserve_cwd
def return_rootdir_pathname(
    _currentdir_pathname=None, _config_yamlfile_name=CONFIG_YAMLFILE_NAME
):
    """Return repo root pathname when executed anywhere within repo.

    Args:
        _currentdir_pathname:
        _config_yamlfile_name:
    """
    if not _currentdir_pathname:
        _currentdir_pathname = os.getcwd()
    while _config_yamlfile_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    return os.getcwd()


@preserve_cwd
def return_rulefile_pathnames_chain_as_list(
    _startdir_pathname=None,
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    _config_yamlfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return list of rule files from parent directories and current directory.

    Looks no higher than root directory of mklists repo.

    Args:
        _startdir_pathname:
        _rule_yamlfile_name:
        _config_yamlfile_name:
    """
    if not _startdir_pathname:
        _startdir_pathname = os.getcwd()
    os.chdir(_startdir_pathname)
    rulefile_pathnames_chain = []
    while _rule_yamlfile_name in os.listdir():
        rulefile_pathnames_chain.insert(
            0, os.path.join(os.getcwd(), _rule_yamlfile_name)
        )
        if _config_yamlfile_name in os.listdir():
            break
        os.chdir(os.pardir)

    return rulefile_pathnames_chain


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
            is_valid_as_filename(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)


def return_yamlstr_from_yamlfile(_yamlfile_name=None):
    """Returns YAML object from given YAML-format file."""
    try:
        return open(_yamlfile_name).read()
    except FileNotFoundError:
        raise YamlFileNotFoundError(f"YAML file {repr(_yamlfile_name)} not found.")


def return_htmldir_pathname(
    _rootdir_pathname=None, _htmldir_name=HTMLDIR_NAME, _currentdir_pathname=None
):
    """Return pathname for folder holding urlified data files.

    Args:
        _rootdir_pathname: Full pathname of mklists repo root directory.
        _htmldir_name:
        _currentdir_pathname:

    Note: uses output of:
    * return_rootdir_pathname() => here: tmpdir

    Example output: '/Users/foobar/github/mylists/.html/a'
    """
    if not _rootdir_pathname:
        raise MissingArgumentError(f"Missing argument '_roodir_pathname'")
    if not _currentdir_pathname:
        _currentdir_pathname = os.getcwd()
    return os.path.join(_rootdir_pathname, _htmldir_name, _currentdir_pathname)
