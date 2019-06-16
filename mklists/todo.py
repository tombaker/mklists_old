"""Todo"""

from .constants import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
from .exceptions import BadYamlRuleError, NoRulesError, RulefileNotFoundError
from .rules import Rule
from .utils import get_pyobj_from_yamlfile


def delete_older_backups():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_delete_older_backups.py
    Count number of backups under this directory:
        Get short name of current data directory (get_cwd_basename).
        Create list of directories under parent directory of backupdir.
            lsd_visible = [item for item in glob.glob('*') if os.path.isdir(item)]
            Example: if backup dir is
                mkrepo/_backups/a/2018-12-31.23414123
            Then parent is
                mkrepo/_backups/a
            Resulting list might be:
                [ '2018-12-31.23414123', '2019-01-01.12155264', '2019-02-02.02265324' ]
    Either:
        while len(lsd_visible) > backups:
            file_to_be_deleted = lsd_visible.pop(0)
            rm file_to_be_deleted
    Or:
        while len(directory_list) > backups:
            dir_to_delete = directory_list.pop(0)
            print(f"rm {dir_to_delete}")
    """


def get_ctxobj_from_config_yamlfile():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_get_ctxobj_from_config_yamlfile
    """


def load_rules_from_yamlfiles(verbose=True):
    """Return list of rule objects from rule files."""

    all_rules_list = []
    config_yamlfile = CONFIG_YAMLFILE_NAME
    rulefile = RULE_YAMLFILE_NAME

    config_pydict = get_pyobj_from_yamlfile(config_yamlfile)
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

    ruleobj_list = []
    for item in all_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobj_list.append(Rule(*item))

    # If no rules, return None or empty list?
    return ruleobj_list


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_certain_listfiles_to_other_directories
    """


def move_existing_listfiles_to_backupdir(backupdir, backups=2):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_existing_listfiles_to_backupdir
    Get number of backups as configuring (config['backups']
        If backups less than two, then backups = 2 ("mandatory")
    Create a backup directory.
        Generate a name for backupdir (make_backupdir_name).
        Make dir: hard-coded parent dirname (_html) plus generated timestamped name.
    Get list of existing visible files in data directory.
    Move all visible files in data directory to backupdir.
        for file in filelist:
            shutil.move(file, backupdir)
    """


def move_certain_listfiles_from_currentdir_to_backupdir(files=None):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_certain_listfiles_to_other_directories
    -- Move existing files from working directory to backupdir.
    """


def write_datadict_to_htmlfiles_in_htmldir(datadict={}, verbose=False):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_datadict_to_htmlfiles_in_htmldir
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through make_htmlstr_from_textstr.
    """


def write_initial_rule_yamlfiles():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_initial_rule_yamlfiles
    """
    pass
