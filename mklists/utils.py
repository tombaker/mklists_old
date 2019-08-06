"""Utilities used by other modules."""

import os
import glob
import re
import yaml
from .booleans import is_valid_as_filename
from .constants import URL_PATTERN_REGEX
from .decorators import preserve_cwd
from .initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .exceptions import BadYamlError, ConfigFileNotFoundError


def return_datadir_pathnames_under_somedir(
    _somedir_pathname=None, _rule_yamlfile_name_name=RULE_YAMLFILE_NAME
):
    """Return list of data directories under a given directory.

    "Data directories": directories with rules files (by default: '.rules').

    Args:
        :_somedir_pathname: Root of directory tree with data directories.
        :_rule_yamlfile_name_name: Name of rule file (by default: '.rules').

    2019-07-22: Two scenarios?
    * mklists run         - runs in all data directories in repo
    * mklists run --here  - runs just in current directory
    """
    if not _somedir_pathname:
        _somedir_pathname = os.getcwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(_somedir_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if _rule_yamlfile_name_name in files:
            datadirs.append(dirpath)
    return datadirs


@preserve_cwd
def return_rootdir_pathname(
    _current_dirname=None, _configfile_name=CONFIG_YAMLFILE_NAME
):
    """Return repo root pathname when executed anywhere within repo.

    Args:

    See
    /Users/tbaker/github/tombaker/mklists/tests/test_utils_return_rootdir_pathname_DONE.py
    """
    if not _current_dirname:
        _current_dirname = os.getcwd()
    while _configfile_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    return os.getcwd()


@preserve_cwd
def return_rule_filenames_chain_as_list(
    _startdir_pathname=None,
    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    _configfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return list of rule files from parent directories and current directory.

    Looks no higher than root directory of mklists repo.

    Args:
        _startdir_pathname:
        _rule_yamlfile_name:
        _configfile_name:
    """
    if not _startdir_pathname:
        _startdir_pathname = os.getcwd()
    os.chdir(_startdir_pathname)
    rulefile_pathnames_chain = []
    while _rule_yamlfile_name in os.listdir():
        rulefile_pathnames_chain.insert(
            0, os.path.join(os.getcwd(), _rule_yamlfile_name)
        )
        if _configfile_name in os.listdir():
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


def _return_pyobj_from_yamlfile(_generic_yamlfile_name=None):
    """Returns Python object parsed from given YAML-format file."""
    try:
        yamlstr = open(_generic_yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(
            f"YAML file {repr(_generic_yamlfile_name)} not found."
        )

    try:
        return yaml.load(yamlstr)
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(_generic_yamlfile_name)}.")


def _return_htmlstr_from_textstr(text_string=None):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in text_string:
        return text_string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', text_string)
