"""Utilities used by other modules."""

import os
import glob
import re
from pathlib import Path
from .booleans import filename_is_valid_as_filename

# ROOTDIR_RULEFILE_NAME,
from .constants import (
    BACKUPS_DIR_NAME,
    CONFIGFILE_NAME,
    DATADIR_RULEFILE_NAME,
    TIMESTAMP_STR,
)
from .decorators import preserve_cwd
from .exceptions import BadRegexError, RepoNotFoundError

# pylint: disable=bad-continuation
# Black disagrees.


@preserve_cwd
def return_rootdir_path(here=None, configfile=CONFIGFILE_NAME):
    """Return root pathname of mklists repo wherever executed in repo."""
    if not here:
        here = Path.cwd()
    directory_chain_upwards = list(Path(here).parents)
    directory_chain_upwards.insert(0, Path.cwd())
    for directory in directory_chain_upwards:
        if configfile in [item.name for item in directory.glob("*")]:
            return Path(directory)
    raise RepoNotFoundError(f"Not a mklists repo - {repr(configfile)} not found.")


@preserve_cwd
def return_backupdir_pathname(
    workdir=None, backupsdir=BACKUPS_DIR_NAME, timestamp=TIMESTAMP_STR
):
    """Return backups Path named for given (or default) working directory."""
    rootdir = return_rootdir_path()
    if not workdir:
        workdir = Path.cwd()
    backup_subdir = str(Path(workdir).relative_to(rootdir)).strip("/").replace("/", "_")
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


def return_datadirs_list(
    given_pathname=None,
    configfile_name=CONFIGFILE_NAME,
    datadir_rulefile_name=DATADIR_RULEFILE_NAME,
):
    """Return list of data directories under a given directory.

    "Data directory" = directory with hidden rule file ('.rules')
    * root directory has global rule file ('rules.cfg') but is
      not a data directory


    Args:
        given_pathname: starting point for finding data subdirectories.

    2019-07-22: Two scenarios?
    * mklists run --all   - runs in all data directories under repo root directory
    * mklists run         - runs in all data directories under current directory
    * mklists run --here  - runs just in current directory
    2020-01-29: What need to filter "hidden" directories (name starting '^.')?
    """
    if not given_pathname:
        given_pathname = os.getcwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(given_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if datadir_rulefile_name in files:
            if configfile_name not in files:
                datadirs.append(Path(dirpath))

    return datadirs


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
