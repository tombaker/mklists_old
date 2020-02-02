"""Apply rules to process datalines."""

import io
import os
import shutil
from pathlib import Path
from .constants import (
    BACKUPS_DIR_NAME,
    CONFIG_YAMLFILE_CONTENT,
    CONFIG_YAMLFILE_NAME,
    DATADIR_NAME,
    DATADIR_RULEFILE_CONTENTS,
    DATADIR_RULEFILE_NAME,
    ROOTDIR_RULEFILE_CONTENTS,
    ROOTDIR_RULEFILE_NAME,
)
from .decorators import preserve_cwd
from .exceptions import NoBackupDirSpecifiedError, RepoAlreadyInitialized
from .utils import (
    return_htmlline_from_textline,
    return_visiblefiles_list,
    return_rootdir_pathname,
)

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
    dira=DATADIR_NAME,
    dira_rulefile=DATADIR_RULEFILE_NAME,
    dira_rulefile_contents=DATADIR_RULEFILE_CONTENTS,
    root_rulefile=ROOTDIR_RULEFILE_NAME,
    root_rulefile_contents=ROOTDIR_RULEFILE_CONTENTS,
):
    """Write starter rule files to root directory and one data directory."""
    Path(dira).mkdir(parents=True, exist_ok=True)
    Path(dira).joinpath(dira_rulefile).write_text(dira_rulefile_contents)
    Path(root_rulefile).write_text(root_rulefile_contents)


@preserve_cwd
def delete_older_backupdirs(
    backups_depth=None, backups_name=BACKUPS_DIR_NAME, rootdir_path=None, dryrun=False
):
    """Delete all but specified number of backups of current working directory."""
    # 2019-01-28: Need function to test sanity of config file settings?
    if not rootdir_path:
        rootdir_path = return_rootdir_pathname()
    if backups_depth is None:
        backups_depth = 0
    dir = Path(rootdir_path).joinpath(backups_name)
    subdirs = []
    for subdir in sorted(Path(dir).glob("*")):
        subdirs.append(subdir)
        to_delete = sorted([subsub for subsub in Path(subdir).glob("*")])[
            :-(backups_depth)
        ]
        for item in to_delete:
            shutil.rmtree(item)
    for subdir in subdirs:
        try:
            subdir.rmdir()  # will delete subdir only if empty
        except OSError:
            pass  # leave subdir if not empty


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
