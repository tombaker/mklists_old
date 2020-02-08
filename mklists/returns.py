"""Utilities used by other modules."""

import os
import glob
import re
from pathlib import Path
from .booleans import filename_is_valid

# ROOTDIR_RULEFILE_NAME,
from .constants import (
    BACKUPS_DIR_NAME,
    CONFIGFILE_NAME,
    DATADIR_RULEFILE_NAME,
    HTMLDIR_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
)
from .decorators import preserve_cwd
from .exceptions import BadRegexError, RepoNotFoundError

# pylint: disable=bad-continuation
# Black disagrees.


def compile_regex(_regex=None):
    """Return compiled regex from regular expression string."""
    try:
        compiled_regex = re.compile(_regex)
    except re.error:
        raise BadRegexError(f"String {repr(_regex)} does not compile as regex.")
    return compiled_regex


@preserve_cwd
def get_backupdir_path(
    workdir=None, backupsdir=BACKUPS_DIR_NAME, timestamp=TIMESTAMP_STR
):
    """Return backups Path named for given (or default) working directory."""
    rootdir = get_rootdir_path()
    if not workdir:
        workdir = Path.cwd()
    backup_subdir = str(Path(workdir).relative_to(rootdir)).strip("/").replace("/", "_")
    return Path(rootdir) / backupsdir / backup_subdir / timestamp


def get_datadir_paths(
    given_pathname=None,
    configfile_name=CONFIGFILE_NAME,
    datadir_rulefile_name=DATADIR_RULEFILE_NAME,
):
    """Return list of data directories below given directory."""
    if not given_pathname:
        given_pathname = Path.cwd()
    datadirs = []
    for dirpath, dirs, files in os.walk(given_pathname):
        dirs[:] = [d for d in dirs if not d[0] == "."]
        if datadir_rulefile_name in files:
            if configfile_name not in files:
                datadirs.append(Path(dirpath))
    return datadirs


def get_htmldir_path(root=None, htmldir=HTMLDIR_NAME, datadir=None):
    """Return pathname for folder holding htmlified data files."""
    if not root:
        root = get_rootdir_path()
    if not htmldir:
        datadir = Path.cwd()
    return os.path.join(root, htmldir, datadir)


@preserve_cwd
def get_rootdir_path(here=None, configfile=CONFIGFILE_NAME):
    """Return root pathname of mklists repo wherever executed in repo."""
    if not here:
        here = Path.cwd()
    directory_chain_upwards = list(Path(here).parents)
    directory_chain_upwards.insert(0, Path.cwd())
    for directory in directory_chain_upwards:
        if configfile in [item.name for item in directory.glob("*")]:
            return Path(directory)
    raise RepoNotFoundError(f"Not a mklists repo - {repr(configfile)} not found.")


def get_visible_filenames():
    """Return list of names of visible files with valid names."""
    all_datafile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            filename_is_valid(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)


def linkify_line(line=None, url_regex=URL_PATTERN_REGEX):
    """Return text lines with URLs wrapped with HREF tags."""
    if "<a href=" in line:
        return line
    return re.compile(url_regex).sub(r'<a href="\1">\1</a>', line.rstrip()) + "\n"
