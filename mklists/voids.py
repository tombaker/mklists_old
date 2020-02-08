"""Apply rules to process datalines."""

import os
import io
import shutil
from pathlib import Path
from .constants import (
    BACKUPS_DIR_NAME,
    CONFIGFILE_CONTENT,
    CONFIGFILE_NAME,
    DATADIR_NAME,
    DATADIR_RULEFILE_CONTENTS,
    DATADIR_RULEFILE_NAME,
    ROOTDIR_RULEFILE_CONTENTS,
    ROOTDIR_RULEFILE_NAME,
)
from .decorators import preserve_cwd
from .exceptions import NoBackupDirSpecifiedError, RepoAlreadyInitialized
from .returns import get_visible_filenames, get_rootdir_path, linkify_textline

# pylint: disable=bad-continuation
# Black disagrees.


def delete_older_backupdirs(
    backups_depth=None, backups_name=BACKUPS_DIR_NAME, rootdir_path=None
):
    """Delete all but specified number of backups of current working directory."""
    if not rootdir_path:
        rootdir_path = get_rootdir_path()
    try:
        backups_depth = abs(int(backups_depth))
    except (ValueError, TypeError):  # eg, "asdf", None...
        backups_depth = 0
    backup_path = Path(rootdir_path).joinpath(backups_name)
    subdirs = []
    for subdir in sorted(Path(backup_path).glob("*")):
        subdirs.append(subdir)
        subsubdirs = []
        for subsubdir in sorted(Path(subdir).glob("*")):
            subsubdirs.insert(0, subsubdir)
        while len(subsubdirs) > backups_depth:
            directory_to_be_deleted = subsubdirs.pop()
            shutil.rmtree(directory_to_be_deleted)
    for subdir in subdirs:
        try:
            subdir.rmdir()  # will delete subdir only if empty
        except OSError:
            pass  # leave subdir if not empty
    # 2020-02-03: Unsure whether...
    # try:
    #     backup_path.rmdir() # will delete only if empty
    # except OSError:
    #     pass      # leave subdir if not empty


@preserve_cwd
def move_all_datafiles_to_backupdir(backupdir=None, datadir=None):
    """Move visible files in given data directory to named backup directory."""
    if not datadir:
        datadir = Path.cwd()
    if not backupdir:
        raise NoBackupDirSpecifiedError(f"No pathname specified for backup directory.")
    os.chdir(datadir)
    try:
        for file in get_visible_filenames():
            shutil.move(file, backupdir)
    except OSError:
        print("Got an exception")


def move_specified_datafiles_elsewhere(
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


@preserve_cwd
def write_htmlfiles(
    name2lines_dict=None, htmldir_pathname=None, backupdir_shortname=None
):
    """Writes contents of in-memory dictionary, urlified, to disk."""
    htmldir_subdir_pathname = os.path.join(htmldir_pathname, backupdir_shortname)
    if not os.path.exists(htmldir_subdir_pathname):
        os.makedirs(htmldir_subdir_pathname)
    os.chdir(htmldir_subdir_pathname)
    for file in get_visible_filenames():
        os.remove(file)
    for key in list(name2lines_dict.keys()):
        lines_to_be_written = []
        for line in name2lines_dict[key]:
            lines_to_be_written.append(linkify_textline(line))
        file_to_write = key + ".html"
        # Pathlib!
        io.open(file_to_write, "w", encoding="utf-8").writelines(lines_to_be_written)


def write_new_datafiles(_name2lines_dict=None):
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


def write_starter_configfile(
    rootdir_pathname=None,
    configfile_name=CONFIGFILE_NAME,
    configfile_content=CONFIGFILE_CONTENT,
):
    """Write initial config file (mklists.yml) to root directory."""
    if not rootdir_pathname:
        rootdir_pathname = os.getcwd()
    file_tobewritten_pathname = os.path.join(rootdir_pathname, configfile_name)
    if os.path.exists(file_tobewritten_pathname):
        raise RepoAlreadyInitialized(
            f"Repo already initialized with {configfile_name}."
        )
    with open(file_tobewritten_pathname, "w", encoding="utf-8") as outfile:
        outfile.write(configfile_content)


def write_starter_rulefiles(
    dira=DATADIR_NAME,
    dira_rulefile=DATADIR_RULEFILE_NAME,
    dira_rulefile_contents=DATADIR_RULEFILE_CONTENTS,
    root_rulefile=ROOTDIR_RULEFILE_NAME,
    root_rulefile_contents=ROOTDIR_RULEFILE_CONTENTS,
):
    """Write starter rule files to root directory and to starter data directory."""
    Path(root_rulefile).write_text(root_rulefile_contents)
    Path(dira).mkdir(parents=True, exist_ok=True)
    Path(dira).joinpath(dira_rulefile).write_text(dira_rulefile_contents)
