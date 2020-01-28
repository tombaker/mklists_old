"""Apply rules to process datalines."""

import io
import os
import shutil
from pathlib import Path
from .constants import (
    CONFIG_YAMLFILE_CONTENT,
    CONFIG_YAMLFILE_NAME,
    DATADIRA_NAME,
    DATADIRA_RULES_CSVFILE_CONTENTS,
    ROOTDIR_RULES_CSVFILE_CONTENTS,
    RULES_CSVFILE_NAME,
)
from .decorators import preserve_cwd
from .exceptions import (
    BackupDepthUnspecifiedError,
    NoBackupDirSpecifiedError,
    RepoAlreadyInitialized,
)
from .utils import return_htmlline_from_textline, return_visiblefiles_list

# pylint: disable=bad-continuation
# Black disagrees.


def write_config_yamlfile(
    rootdir_pathname=None,
    config_yamlfile_name=CONFIG_YAMLFILE_NAME,
    config_yamlfile_content=CONFIG_YAMLFILE_CONTENT,
):
    """Write initial YAML config file, 'mklists.yml', to root directory."""
    if not rootdir_pathname:
        rootdir_pathname = os.getcwd()
    file_tobewritten_pathname = os.path.join(rootdir_pathname, config_yamlfile_name)
    if os.path.exists(file_tobewritten_pathname):
        raise RepoAlreadyInitialized(
            f"Repo already initialized with {config_yamlfile_name}."
        )
    with open(file_tobewritten_pathname, "w", encoding="utf-8") as outfile:
        outfile.write(config_yamlfile_content)


@preserve_cwd
def write_rules_csvfiles(
    rules_csvfile_name=RULES_CSVFILE_NAME,
    datadira_rules_csvfile_contents=DATADIRA_RULES_CSVFILE_CONTENTS,
    datadira_name=DATADIRA_NAME,
    rootdir_rules_csvfile_contents=ROOTDIR_RULES_CSVFILE_CONTENTS,
):
    """@@@Docstring"""
    io.open(rules_csvfile_name, "w", encoding="utf-8").write(
        rootdir_rules_csvfile_contents
    )
    os.mkdir(datadira_name)
    os.chdir(datadira_name)
    io.open(rules_csvfile_name, "w", encoding="utf-8").write(
        datadira_rules_csvfile_contents
    )


@preserve_cwd
def delete_older_backupdirs(backupdir=None, backup_depth=None):
    """Delete all but specified number of backups of current working directory."""
    if backup_depth is None:
        raise BackupDepthUnspecifiedError(f"Number of backups to keep is unspecified.")
    os.chdir(backupdir)
    ls_backupdir = sorted(os.listdir())
    while len(ls_backupdir) > backup_depth:
        timestamped_dir_to_delete = ls_backupdir.pop(0)
        shutil.rmtree(timestamped_dir_to_delete)
        print(f"rm {timestamped_dir_to_delete}")


@preserve_cwd
def move_all_datafiles_to_backupdir(backupdir=None, datadir=None):
    """Move visible files in given data directory to named backup directory."""
    if not datadir:
        datadir = Path.cwd()
    if not backupdir:
        raise NoBackupDirSpecifiedError(f"No pathname specified for backup directory.")
    os.chdir(datadir)
    try:
        for file in return_visiblefiles_list():
            shutil.move(file, backupdir)
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
