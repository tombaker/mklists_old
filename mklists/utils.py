"""Utilities used by other modules"""

import os
import re
import glob
from mklists import (
    CONFIGFILE_NAME,
    INVALID_FILENAME_PATTERNS,
    RULEFILE_NAME,
    TIMESTAMP_STR,
    URL_PATTERN_REGEX,
    VALID_FILENAME_CHARACTERS_REGEX,
    BadFilenameError,
    ConfigFileNotFoundError,
)


def get_backupdir_name(now=TIMESTAMP_STR, listdir_name=None):
    """@@@Docstring"""
    return os.path.join(listdir_name, now)


def get_htmlstr_from_textstr(string):
    """Return string with URLs wrapped in A_HREF tags."""
    if "<a href=" in string:
        return string
    return re.compile(URL_PATTERN_REGEX).sub(r'<a href="\1">\1</a>', string)


def get_listdir_names_under_rootdir(rootdir_name="."):
    """Return list of all data directories under a given root directory.
    By definition, a data directory is a directory with a '.rules' file."""
    listdirs = []
    for (dirpath, __, filenames) in os.walk(rootdir_name):
        if RULEFILE_NAME in filenames:
            listdirs.append(os.path.join(dirpath))
    return listdirs


def get_listdir_shortname(listdir=os.getcwd(), rootdir=None):
    return listdir[len(rootdir) :].strip("/").replace("/", "_")


def get_listfile_names(listdir_name=os.getcwd()):
    """Return names of visible files with names that are valid as listfiles."""
    os.chdir(listdir_name)
    all_listfile_names = []
    for filename in [name for name in glob.glob("*") if os.path.isfile(name)]:
        if not has_valid_name(filename):
            raise BadFilenameError(f"{repr(filename)} has bad characters or patterns.")
        all_listfile_names.append(filename)
    return all_listfile_names


def get_rootdir_name(path="."):
    """Return project rootdir when executed in the rootdir or in a listdir."""
    os.chdir(path)
    while True:
        ls_cwd = os.listdir()
        if RULEFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
            continue
        else:
            break

    if CONFIGFILE_NAME in os.listdir():
        return os.getcwd()
    else:
        raise ConfigFileNotFoundError(f"No {CONFIGFILE_NAME} found. Try mklists init.")


def has_valid_name(filename, badpats=INVALID_FILENAME_PATTERNS):
    """Return True if filename has no invalid characters or string patterns.
    @@@Figure out how to pass in invalid filename patterns from context."""
    for badpat in badpats:
        if re.search(badpat, filename):
            return False
    for char in filename:
        if not bool(re.search(VALID_FILENAME_CHARACTERS_REGEX, char)):
            return False
    return True


def update_settings_dict(settings_dict=None, overrides=None):
    """Inject dictionary B into A, ignoring keys in B with value None."""
    overrides = {key: overrides[key] for key in overrides if overrides[key] is not None}
    settings_dict.update(overrides)
    return settings_dict


def write_yamlstr_to_yamlfile(yamlstr, yamlfile_name):
    """Write YAML string to YAML file."""
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def move_old_listfiles_to_backupdir(backupdir, backups=2):
    """
    if backups is less than two, then backups = 2 - "mandatory"
    If 'backup' is True:
    before writing data_dict contents to disk,
    creates timestamped backup directory in specified backup_dir,
    and moves all visible files in data directory to backup directory.
    Make time-stamped directory in BACKUP_DIR_NAME (create constant!)
    Create: backup_dir_timestamped = os.path.join(backup_dir, TIMESTAMP_STR)
    Move existing files to backup_dir
    Delete oldest backups:
    delete_oldest_backup(backup_dir, backups):
        lsd_visible = [item for item in glob.glob('*')
                       if os.path.isdir(item)]
        while len(lsd_visible) > backups:
            file_to_be_deleted = get_lsvisible_names.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)

    Note: there should never be a situation where listfiles have
    been deleted and the data in memory has not yet been written to disk.
    Therefore, there should _always_ be at least one backup."""
