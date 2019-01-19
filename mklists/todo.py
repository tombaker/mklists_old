"""Todo"""

from mklists import (
    CONFIGFILE_NAME,
    RULEFILE_NAME,
    RulefileNotFoundError,
    NoRulesError,
    BadYamlRuleError,
)
from .rules import Rule
from .utils import get_pyobj_from_yamlfile


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def move_existing_listfiles_to_backupdir(backupdir, backups=2):
    """
    if backups is less than two, then backups = 2 - "mandatory"
    If 'backup' is True:
    before writing datadict contents to disk,
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


def get_ruleobjs_list_from_yaml_rulefiles(
    configfile=CONFIGFILE_NAME, rulefile=RULEFILE_NAME, verbose=True
):
    """Return list of rule objects from configuration and rule files."""
    # If no rules, return None or empty list?

    all_rules_list = []
    config_pydict = get_pyobj_from_yamlfile(configfile)
    try:
        all_rules_list.append(config_pydict["global_rules"])
    except KeyError:
        if verbose:
            print("No global rules found - skipping.")
    except TypeError:
        if verbose:
            print("No global rules found - skipping.")

    rules_pylist = get_pyobj_from_yamlfile(rulefile)
    try:
        all_rules_list.append(rules_pylist)
    except FileNotFoundError:
        raise RulefileNotFoundError(f"Rule file {repr(rulefile)} was not found.")

    if not all_rules_list:
        raise NoRulesError("No rules were found.")

    ruleobjs_list = []
    for item in all_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobjs_list.append(Rule(*item))

    return ruleobjs_list


def write_datadict_to_htmlfiles(datadict={}, verbose=False):
    """Belongs in makelists.py:
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through make_htmlstr_from_textstr."""


def write_datadict_to_listfiles(datadict=None, verbose=False):
    """Belongs in makelists.py:
    -- Move existing files from working directory to backupdir.
    -- Write out contents of datadict to working directory:
       -- datadict keys are names of files.
       -- datadict values are contents of files."""
