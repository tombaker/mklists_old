"""Read-write module

Functions with side effects such as:
* reading files from disk (including config and rule files)
* writing to files on disk
* modifying data structures in memory"""


import os
import yaml
from mklists import (
    GLOBAL_DIR,
    LOCAL_DIR,
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILE_STARTER_YAMLSTR,
    BadFilenameError,
    BadYamlError,
    BadYamlRuleError,
    BlankLinesError,
    DatadirHasNonFilesError,
    InitError,
    NoDataError,
    NotUTF8Error,
)
from mklists.ruleclass import Rule
from mklists.utils import read_yamlfile_to_pyobject, is_file, has_valid_name


def find_rulefiles():
    """GLOBAL_RULEFILE_NAME
    LOCAL_RULEFILE_NAME
    MKLISTS_YML_NAME

    Repository
    mydir/mklists.yaml - configuration
    mydir/.globalrules - global rules
    mydir/a/.rules     - list A rules
    mydir/b/.rules     - list B rules

    Rule- and config-finding algorithm:
    a. Look for mklists.yaml
       * in current directory, then
       * in parent directory
    b. When mklists.yaml found (i.e., in root directory)
       * look in root directory for (optional) .globalrules
       * look under all subdirectories for .rules files"""
    # if os.path.exists(GLOBAL_RULEFILE_NAME):
    # for directory_name, file_name in [
    #    (GLOBAL_DIR,
    #    (LOCAL_DIR, LOCAL_RULEFILE_NAME),
    # ]:
    #    rulefile = os.path.join(directory_name, file_name)
    #        os.makedirs(directory_name)


def get_rules(valid_filename_chars, invalid_filename_patterns):
    """Find and load YAML rulefiles, returning Python list of rule objects."""

    aggregated_rules_list = []
    for rulefile_name in global_rulefile_name, local_rulefile_name:
        if rulefile_name:
            rules_list = read_yamlfile_to_pyobject(rulefile_name)
            aggregated_rules_list = aggregated_rules_list + rules_list
    ruleobj_list = []
    for item in aggregated_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobj_list.append(Rule(*item))

    return ruleobj_list


def get_rules2(lrules=LOCAL_RULEFILE_NAME, grules=GLOBAL_RULEFILE_NAME):
    rules_list = []
    try:
        rules_to_add = read_yamlfile_to_pyobject(grules)
        rules_list.append(rules_to_add)
    except FileNotFoundError:
        print("File was not found")
    except TypeError:
        print("NoneType")
    return rules_list


def get_datalines():
    """Returns lines from files with valid names, UTF8, with no blank lines."""

    all_lines = []
    for path_name in ls_visible():
        if not has_valid_name(path_name):
            raise BadFilenameError
        if not is_file(path_name):
            print("Mklists data directories must contain files only.")
            raise DatadirHasNonFilesError(f"{repr(path_name)} is not a file.")
        try:
            file_lines = open(path_name).readlines()
        except UnicodeDecodeError:
            print("All visible files in data directory must be UTF8-encoded.")
            raise NotUTF8Error(f"{repr(path_name)} is not in UTF8-encoded.")

        for line in file_lines:
            if not line.rstrip():
                print("Files in data directory must contain no blank lines.")
                raise BlankLinesError(f"{repr(path_name)} has blank lines.")

    if not all_lines:
        raise NoDataError("No data to process!")

    return all_lines


def get_lines_valid_list_file(path_name):
    """Returns if pathname has valid name, is UTF8, has no blank lines."""

    return True


def move_datafiles_to_backup(backup_depth=None):
    """
    If 'backup' is ON:
    before writing data_dict contents to disk,
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

    Note: there should never be a situation where datafiles have
    been deleted and the data in memory has not yet been written to disk.
    Therefore, there should _always_ be at least one backup."""


def write_data_dict_to_diskfiles(data_dict=None, verbose=False):
    """If 'backup' is ON, move existing files from working to backup directory.
    If 'backup' is OFF, DELETE existing files in working directory.
    Write data_dict to working directory:
    -- data_dict keys are names of files.
    -- data_dict values are contents of files."""


def write_data_dict_urlified_to_diskfiles(data_dict={}, verbose=False):
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
