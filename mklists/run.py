"""Apply rules to process datalines."""

from collections import defaultdict
from .constants import CONFIG_YAMLFILE_NAME, RULE_YAMLFILE_NAME
from .exceptions import (
    BadYamlRuleError,
    BlankLinesError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RulefileNotFoundError,
)
from .rules import Rule
from .utils import get_pyobj_from_yamlfile, is_line_match_to_rule


def apply_rules_to_datalines(ruleobj_list=None, dataline_list=None):
    """Applies rules, one by one, to process an aggregated list of datalines.

    Args:
        ruleobj_list: list of rule objects
        dataline_list: list of strings (all data lines)

    Returns:
        datadict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    datadict = defaultdict(list)
    first_key_is_initialized = False

    if not ruleobj_list:
        raise NoRulesError("No rules specified.")

    if not dataline_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in datadict.
    for ruleobj in ruleobj_list:

        # Initialize datadict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            datadict[ruleobj.source] = dataline_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in datadict[ruleobj.source]:
            if is_line_match_to_rule(ruleobj, line):
                datadict[ruleobj.target].extend([line])
                datadict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(datadict[ruleobj.target])
            ]
            decorated.sort()
            datadict[ruleobj.target] = [line for (___, __, line) in decorated]

    return dict(datadict)


def delete_older_backups():
    """
    Count number of backups under this directory:
        Get short name of current data directory (get_listdir_shortname).
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


def get_dataline_list_from_listfiles(listfile_names=None):
    """Returns lines from files with valid names, UTF8, with no blank lines."""
    all_datalines = []
    for listfile in listfile_names:
        try:
            listfile_lines = open(listfile).readlines()
        except UnicodeDecodeError:
            raise NotUTF8Error(f"{repr(listfile)} is not UTF8-encoded.")
        for line in listfile_lines:
            if not line.rstrip():
                print("Files in data directory must contain no blank lines.")
                raise BlankLinesError(f"{repr(listfile)} has blank lines.")
        all_datalines.extend(listfile_lines)

    if not all_datalines:
        raise NoDataError("No data to process!")
    return all_datalines


def get_ruleobj_list_from_rule_yamlfiles(verbose=True):
    """Return list of rule objects from configuration and rule files."""
    # If no rules, return None or empty list?

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

    return ruleobj_list


def move_certain_listfiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)"""


def move_existing_listfiles_to_backupdir(backupdir, backups=2):
    """
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


def write_datadict_to_htmlfiles_in_htmldir(datadict={}, verbose=False):
    """
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through make_htmlstr_from_textstr.
    """


def write_datadict_to_listfiles_in_currentdir(datadict=None, verbose=False):
    """
    -- Move existing files from working directory to backupdir.
    -- Write out contents of datadict to working directory:
       -- datadict keys are names of files.
       -- datadict values are contents of files.
    """
