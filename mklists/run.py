"""Apply rules to process datalines."""


import io
import os
import shutil
from collections import defaultdict
import pytest
from .booleans import dataline_is_match_to_ruleobj
from .config import Defaults
from .decorators import preserve_cwd
from .exceptions import (
    BackupDepthUnspecifiedError,
    BadRuleError,
    BlankLinesError,
    NoBackupDirSpecifiedError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RulefileNotFoundError,
)
from .rules import Rule
from .utils import (
    return_yamlobj_from_yamlstr,
    return_yamlstr_from_yamlfile,
    return_backupdir_shortname,
    return_htmlline_from_textline,
    return_visiblefiles_list,
)


@preserve_cwd
def delete_older_backupdirs(
    _rootdir_pathname=None,
    _backupdir_subdir_name=None,
    _backupdir_shortname=None,
    _backup_depth_int=None,
):
    """Delete all but X number of backups of current working directory.

    Args:
        _rootdir_pathname:
        _backupdir_subdir_name:
        _backupdir_shortname:
        _backup_depth_int: Number of backups to keep [default: 2]

    See /Users/tbaker/github/tombaker/mklists/tests/test_backups_delete_older_backupdirs_TODO.py
    """
    if _backup_depth_int is None:
        raise BackupDepthUnspecifiedError(f"Number of backups to keep is unspecified.")
    backupdir = os.path.join(
        _rootdir_pathname, _backupdir_subdir_name, _backupdir_shortname
    )
    os.chdir(backupdir)
    ls_backupdir = sorted(os.listdir())
    while len(ls_backupdir) > _backup_depth_int:
        timestamped_dir_to_delete = ls_backupdir.pop(0)
        shutil.rmtree(timestamped_dir_to_delete)
        print(f"rm {timestamped_dir_to_delete}")


@pytest.mark.improve
@preserve_cwd
def move_all_datafiles_to_backupdir(
    _datadir_pathname=None, _datafiles_names=None, _backupdir_pathname=None
):
    """Move data files to backup directory.

    "Data files" are all visible files in the data directory.

    Args:
        _datadir_pathname: Pathname of the data directory,
          (typically? always?) the current working directory.
        _datafiles_names: Names of all visible files in the data
          directory (pre-checked to ensure they are text files?).
        _backupdir_pathname: Pathname of the backup directory.
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    if not _backupdir_pathname:
        raise NoBackupDirSpecifiedError(f"No pathname for backup directory specified.")
    os.chdir(_datadir_pathname)
    try:
        for file in _datafiles_names:
            shutil.move(file, _backupdir_pathname)
    except OSError:
        print("Got an exception")


def move_specified_datafiles_to_somedirs(
    _filenames2dirnames_dict=None, _rootdir_pathname=None
):
    """Moves data files to specified destination directories.

    Uses a dictionary, configurable in 'mklists.yml', in which:
    * filenames without a leading slash are relative to the root
      directory of the mklists repo.
    * filenames with a leading slash are relative to the whole
      filesystem, which may result in their being moved out of
      the mklists repo.
    * names of non-existent files are simply ignored.

    Args:
        _filenames2dirnames_dict: keys are filenames, values are destination directories
    """
    for key in _filenames2dirnames_dict:
        destination_dir = os.path.join(_rootdir_pathname, _filenames2dirnames_dict[key])
        if os.path.exists(key):
            if os.path.exists(destination_dir):
                shutil.move(key, destination_dir)


def return_datalines_list_from_datafiles(_datafiles_names=None):
    """Returns lines from files with valid names, UTF8, with no blank lines."""
    all_datalines = []
    for datafile in _datafiles_names:
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


def return_name2lines_dict_by_applying_ruleobjs(
    _ruleobjs_list=None, _datalines_list=None
):
    """Applies rules, one by one, to process aggregated datalines.

    Args:
        _ruleobjs_list: list of rule objects
        _datalines_list: list of strings (all data lines)

    Returns:
        datadict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    datadict = defaultdict(list)
    first_key_is_initialized = False

    if not _ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not _datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in datadict.
    for ruleobj in _ruleobjs_list:

        # Initialize datadict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            datadict[ruleobj.source] = _datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in datadict[ruleobj.source]:
            if dataline_is_match_to_ruleobj(ruleobj, line):
                datadict[ruleobj.target].extend([line])
                datadict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(datadict[ruleobj.target])
            ]
            decorated.sort()
            datadict[ruleobj.target] = [line for (___, __, line) in decorated]

    return dict(datadict)


def write_datafiles_from_name2lines_dict(_name2lines_dict=None):
    """Writes contents of filenames2datalines dictionary in which:
    * keys are names of files that will be created
    * values are (non-empty) contents of such files (lists of text lines)

    Note: assumes that filenames2datalines dictionary is correct:
    * filenames are valid (e.g., no pathname slashes '/')

    Args:
        _name2lines_dict: dictionary relating strings to lists
    """
    for (key, value) in _name2lines_dict.items():
        if value:
            with open(key, "w", encoding="utf-8") as fout:
                fout.writelines(value)


@preserve_cwd
def write_htmlfiles_from_name2lines_dict(
    name2lines_dict=None, htmldir_pathname=None, backupdir_shortname=None
):
    """Writes contents of in-memory dictionary, urlified, to disk.

    Args:
        name2lines_dict: Python dictionary in which:
            * keys are the names of files to be written
            * values are lists of text lines.
        htmldir_pathname: Name of HTML directory (relative to the root directory).
        backupdir_shortname:
    """
    htmldir_subdir_pathname = os.path.join(htmldir_pathname, backupdir_shortname)
    if not os.path.exists(htmldir_subdir_pathname):
        os.makedirs(htmldir_subdir_pathname)
    os.chdir(htmldir_subdir_pathname)

    for file in return_visiblefiles_list():
        os.remove(file)

    for key in list(name2lines_dict.keys()):
        lines_to_be_written = []
        for line in name2lines_dict[key]:
            lines_to_be_written.append(return_htmlline_from_textline(line))

        file_to_write = key + ".html"
        io.open(file_to_write, "w", encoding="utf-8").writelines(lines_to_be_written)
