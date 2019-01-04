"""Read-write module

Functions with side effects such as:
* reading files from disk (including config and rule files)
* writing to files on disk
* modifying data structures in memory"""

from mklists import CONFIGFILE_NAME, BlankLinesError, NoDataError, NotUTF8Error
from mklists.utils import read_yaml_configfile_to_pyobject


def get_datalines(datafile_names: list):
    """Returns lines from files with valid names, UTF8, with no blank lines."""

    all_datalines = []
    for datafile in datafile_names:
        try:
            datafile_lines = open(datafile).readlines()
        except UnicodeDecodeError:
            print("All visible files in data directory must be UTF8-encoded.")
            raise NotUTF8Error(f"{repr(datafile)} is not in UTF8-encoded.")

        for line in datafile_lines:
            if not line.rstrip():
                print("Files in data directory must contain no blank lines.")
                raise BlankLinesError(f"{repr(datafile)} has blank lines.")

        all_datalines.extend(datafile_lines)

    if not all_datalines:
        raise NoDataError("No data to process!")

    return all_datalines


def get_lines_valid_list_file(path_name):
    """Returns if pathname has valid name, is UTF8, has no blank lines."""

    return True


def move_old_datafiles_to_backupdirs(backup_depth=None):
    """
    If 'backup' is True:
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
            file_to_be_deleted = ls_visible_files.pop()
            rm file_to_be_deleted
    for file in filelist:
        shutil.move(file, backup_dir)

    Note: there should never be a situation where datafiles have
    been deleted and the data in memory has not yet been written to disk.
    Therefore, there should _always_ be at least one backup."""


def write_dataobj_to_textfiles(data_dict=None, verbose=False):
    """If 'backup' is ON, move existing files from working to backup directory.
    If 'backup' is OFF, DELETE existing files in working directory.
    Write data_dict to working directory:
    -- data_dict keys are names of files.
    -- data_dict values are contents of files."""


def write_dataobj_to_htmlfiles(data_dict={}, verbose=False):
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


def move_certain_datafiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def get_rules():
    """Find and load YAML rulefiles, returning Python list of rule objects."""

    # aggregated_rules_list = []
    # for rulefile_name in RULEFILE_NAME, LOCAL_RULEFILE_NAME:
    #     if rulefile_name:
    #         rules_list = read_yaml_configfile_to_pyobject(rulefile_name)
    #         aggregated_rules_list = aggregated_rules_list + rules_list

    ruleobj_list = []
    # for item in aggregated_rules_list:
    #    try:
    #        Rule(*item).is_valid
    #    except TypeError:
    #        raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
    #    ruleobj_list.append(Rule(*item))

    return ruleobj_list


def get_rules2():
    """@@@Docstring"""
    rules_list = []
    try:
        rules_to_add = read_yaml_configfile_to_pyobject(CONFIGFILE_NAME)
        rules_list.append(rules_to_add)
    except FileNotFoundError:
        print("File was not found")
    except TypeError:
        print("NoneType")
    return rules_list
