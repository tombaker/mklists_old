"""Read-write module

Functions with side effects such as:
* reading files from disk
* writing to files on disk
* modifying data structures in memory
"""

import os
import re
import string
import sys
import pprint
import yaml
from mklists import (
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILE_STARTER_YAMLSTR,
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARS_STR,
    BadFilenameError,
    BadYamlError,
    BadYamlRuleError,
    BlankLinesError,
    ConfigFileNotFoundError,
    DatadirHasNonFilesError,
    InitError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
)
from mklists.rules import Rule


def read_overrides_from_file(configfile_name):
    """docstring"""
    return yaml.load(open(configfile_name).read())


def apply_overrides(settings_dict, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {
        key: overrides[key] for key in overrides if overrides[key] is not None
    }
    settings_dict.update(overrides)
    return settings_dict


def write_yamlstr_to_yamlfile(yamlfile_name, yamlstr):
    """Writes string in YAML format to file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def read_yamlfile_return_pyobject(yamlfile_name):
    """Returns Python object parsed from YAML-format file."""
    try:
        return yaml.safe_load(open(yamlfile_name))
    except yaml.YAMLError:
        raise BadYamlError(f"Bad YAML format in {repr(yamlfile_name)}.")


def get_datalines(ls_visible=[], but_not=None):
    """Returns aggregated list of lines from data files.

    Mklists is very strict about contents of data directory.
    All exceptions encountered in this function, in _get_file(),
    and in any of the functions called by _get_file(), will
    result in exit from the program, with an error message about
    what the user will need to correct in order to get it to run."""
    datalines = []
    for item in ls_visible:
        datalines.append(_get_filelines(item, invalid_patterns=but_not))
        if verbose:
            print(f"Reading {repr(item)}.")
            print(datalines)  # 2018-09-02: just for debugging
    if not datalines:
        raise NoDataError("No data to process!")
    return datalines


def _get_filelines(thing_in_directory, invalid_patterns=None):
    all_lines = []
    if not is_file(thing_in_directory):
        print("All visible objects in current directory must be files.")
        raise DatadirHasNonFilesError(f"{thing_in_directory} is not a file.")
    if not has_valid_name(thing_in_directory, invalid_patterns):
        print(
            "Invalid filename patterns are intended to detect the "
            "presence of backup files, temporary files, and the like."
        )
        raise BadFilenameError(
            f"{repr(thing_in_directory)} matches one of " "{invalid_patterns}."
        )
    if not is_utf8_encoded(thing_in_directory):
        print("All visible files in data directory must be UTF8-encoded.")
        raise NotUTF8Error(f"File {thing_in_directory} is not UTF8-encoded.")
    with open(thing_in_directory) as rfile:
        for line in rfile:
            if not line:
                raise BlankLinesError(
                    f"{thing_in_directory} is not valid as "
                    "data because it has blank lines."
                )
            all_lines.append(line)

    return all_lines


def move_datafiles_to_backup(backup_depth=None):
    """
    Make time-stamped directory in BACKUP_DIR_NAME (create constant!)
    Create: backup_dir_timestamped = '/'.join([backup_dir, TIMESTAMP_STR])
    Move existing files to backup_dir
    Delete oldest backups:
    delete_oldest_backup(backup_dir, backup_depth):
        lsd_visible = [item for item in glob.glob('*')
                       if os.path.isdir(item)]
        while len(lsd_visible) > backup_depth:
            file_to_be_deleted = ls_visible.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)
    """


def write_data_to_files(datalines_d=None, verbose=False):
    pass


# Write urlified data files to urlify_dir.
def write_data_urlified_to_files(
    datalines_d={}, urlify_dir=None, verbose=False
):
    """Something like: def removefiles(targetdirectory):
    pwd = os.getcwd()
    abstargetdir = absdirname(targetdirectory)
    if os.path.isdir(abstargetdir):
        os.chdir(abstargetdir)
        files = datals()
        if files:
            for file in files:
                os.remove(file)
        os.chdir(pwd)
    """
    print(f"* Move files outside datadir as per ['files2dirs'].")


def move_files_to_external_directories(files2dirs_dict=None):
    """
    Args:
        files2dirs_dict: filename (key) and destination directory (value)
    """
