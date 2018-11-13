"""Read-write module

Functions with side effects such as:
* reading files from disk
* writing to files on disk
* modifying data structures in memory
"""

import yaml
from mklists import (
    BadFilenameError,
    BadYamlError,
    BlankLinesError,
    DatadirHasNonFilesError,
    NoDataError,
    NotUTF8Error,
)
from mklists.utils import is_file, has_valid_name, is_utf8_encoded


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
    If 'backup' is ON:
    before writing mklists_dict contents to disk,
    creates timestamped backup directory in specified backup_dir,
    and moves all visible files in data directory to backup directory.
    Make time-stamped directory in BACKUP_DIR_NAME (create constant!)
    Create: backup_dir_timestamped = '/'.join([backup_dir, TIMESTAMP_STR])
    Move existing files to backup_dir
    Delete oldest backups:
    delete_oldest_backup(backup_dir, backups):
        lsd_visible = [item for item in glob.glob('*')
                       if os.path.isdir(item)]
        while len(lsd_visible) > backups:
            file_to_be_deleted = ls_visible.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)
    """


def write_mklists_dict_to_diskfiles(data_dict=None, verbose=False):
    """If 'backup' is ON, move existing files from working to backup directory.
    If 'backup' is OFF, DELETE existing files in working directory.
    Write mklists_dict to working directory:
    -- mklists_dict keys are names of files.
    -- mklists_dict values are contents of files."""


def write_mklists_dict_urlified_to_file(data_dict={}, verbose=False):
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


def move_files_to_given_destinations(files2dirs_dict=None):
    """
    Args:
        files2dirs_dict: filename (key) and destination directory (value)
    """
