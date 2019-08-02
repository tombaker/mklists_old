"""Utilities used by other modules."""

import os
import re
import glob
from .booleans import is_valid_as_filename
from .decorators import preserve_cwd
from .initialize import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .exceptions import ConfigFileNotFoundError


def return_datadir_pathnames_under_somedir(
    somedir_pathname=None, rulefile_name=RULE_YAMLFILE_NAME
):
    """Return list of data directories under a given directory.

    "Data directories": directories with rules files (by default: '.rules').

    Args:
        :somedir_pathname: Root of directory tree with data directories.
        :rulefile_name: Name of rule file (by default: '.rules').

    2019-07-22: Two scenarios?
    * mklists run         - runs in all data directories in repo
    * mklists run --here  - runs just in current directory
    """
    if not somedir_pathname:
        somedir_pathname = os.getcwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(somedir_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if rulefile_name in files:
            datadirs.append(dirpath)
    return datadirs


@preserve_cwd
def return_rootdir_pathname(cwd=None, configfile_name=CONFIG_YAMLFILE_NAME):
    """Return repo root pathname when executed anywhere within repo.

    Args:

    See
    /Users/tbaker/github/tombaker/mklists/tests/test_utils_return_rootdir_pathname_DONE.py
    """
    if not cwd:
        cwd = os.getcwd()
    while configfile_name not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            raise ConfigFileNotFoundError("No config file found - not a mklists repo.")
    else:
        return os.getcwd()


@preserve_cwd
def return_rule_filenames_chain_as_list(
    start_pathname=None,
    rulefile_name=RULE_YAMLFILE_NAME,
    configfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return list of rule files from parent directories and current directory.

    Looks no higher than root directory of mklists repo.

    Args:
        :start_pathname:
        :rulefile_name:
        :configfile_name:
    """
    if not start_pathname:
        start_pathname = os.getcwd()
    os.chdir(start_pathname)
    rulefile_pathnames_chain = []
    while rulefile_name in os.listdir():
        rulefile_pathnames_chain.insert(0, os.path.join(os.getcwd(), rulefile_name))
        if configfile_name in os.listdir():
            break
        os.chdir(os.pardir)

    return rulefile_pathnames_chain


@preserve_cwd
def return_visiblefiles_list(datadir_name=None):
    """Return list of names of visible files with valid names.

    See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
    """
    if not datadir_name:
        datadir_name = os.getcwd()
    os.chdir(datadir_name)
    all_datafile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            is_valid_as_filename(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)
