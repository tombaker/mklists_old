"""Various functions that return a value."""

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
from .exceptions import BadRegexError, ConfigFileNotFoundError, MissingArgumentError

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
def get_backupdir_path(datadir=None, backdir=BACKUPS_DIR_NAME, now=TIMESTAMP_STR):
    """Return backups Path named for given (or default) working directory."""
    rootdir = get_rootdir_path()
    if not datadir:
        datadir = Path.cwd()
    backup_subdir = str(Path(datadir).relative_to(rootdir)).strip("/").replace("/", "_")
    return Path(rootdir) / backdir / backup_subdir / now


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


def get_htmldir_path(rootdir=None, htmldir=HTMLDIR_NAME, datadir=None):
    """Return pathname for folder holding htmlified data files."""
    if not rootdir:
        rootdir = get_rootdir_path()
    if not datadir:
        datadir = Path.cwd()
    if not htmldir:
        raise MissingArgumentError(f"Leave htmldir unspecified to use default ")
    html_subdir = Path(datadir).relative_to(rootdir)
    return Path(rootdir).joinpath(htmldir, html_subdir)


@preserve_cwd
def get_rootdir_path(here=None, mkyml=CONFIGFILE_NAME):
    """Return root pathname of mklists repo wherever executed in repo."""
    if not here:
        here = Path.cwd()
    parents = list(Path(here).parents)
    parents.insert(0, Path.cwd())
    for directory in parents:
        if mkyml in [item.name for item in directory.glob("*")]:
            return Path(directory)
    raise ConfigFileNotFoundError(f"{repr(mkyml)} not found.")


def get_visible_filenames():
    """Return list of names of visible files with valid names."""
    all_datafile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        try:
            filename_is_valid(filename)
        finally:
            all_datafile_names.append(filename)
    return sorted(all_datafile_names)


def linkify_textline(line=None, url_regex=URL_PATTERN_REGEX):
    """Return text lines with URLs wrapped with HREF tags."""
    if "<a href=" in line or "<A HREF=" in line:
        return line
    return re.compile(url_regex).sub(r'<a href="\1">\1</a>', line.rstrip()) + "\n"
