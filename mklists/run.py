"""Apply rules to process datalines."""


import os
import shutil
from collections import defaultdict
import pytest
from .booleans import is_match_to_rule_as_line
from .constants import CONFIG_YAMLFILE_NAME, TIMESTAMP_STR
from .decorators import preserve_cwd
from .exceptions import (
    BackupDepthUnspecifiedError,
    BadYamlRuleError,
    BlankLinesError,
    NoBackupDirSpecifiedError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RulefileNotFoundError,
)
from .rules import Rule
from .utils import return_pyobj_from_yamlstr, return_yamlstr_from_yamlfile


@preserve_cwd
def delete_older_backups(
    _rootdir_pathname=None,
    _backupdir_subdir_name=None,
    _backupdir_shortname=None,
    _backup_depth_int=None,
):
    """Delete all but X number of backups of current working directory.

    Args:
        _rootdir_pathname:
        _backupdir_subdir_name:
        _backupdir_shortname:
        _backup_depth_int: Number of backups to keep [default: 2]

    See /Users/tbaker/github/tombaker/mklists/tests/test_backups_delete_older_backups_TODO.py
    """
    if _backup_depth_int is None:
        raise BackupDepthUnspecifiedError(f"Number of backups to keep is unspecified.")
    backupdir = os.path.join(
        _rootdir_pathname, _backupdir_subdir_name, _backupdir_shortname
    )
    os.chdir(backupdir)
    ls_backupdir = sorted(os.listdir())
    while len(ls_backupdir) > _backup_depth_int:
        timestamped_dir_to_delete = ls_backupdir.pop(0)
        shutil.rmtree(timestamped_dir_to_delete)
        print(f"rm {timestamped_dir_to_delete}")


@pytest.mark.improve
@preserve_cwd
def move_datafiles_to_backupdir(
    _datadir_pathname=None, _datafiles_names=None, _backupdir_pathname=None
):
    """Move data files to backup directory.

    "Data files" are all visible files in the data directory.

    Args:
        _datadir_pathname: Pathname of the data directory,
          (typically? always?) the current working directory.
        _datafiles_names: Names of all visible files in the data
          directory (pre-checked to ensure they are text files?).
        _backupdir_pathname: Pathname of the backup directory.
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    if not _backupdir_pathname:
        raise NoBackupDirSpecifiedError(f"No pathname for backup directory specified.")
    os.chdir(_datadir_pathname)
    try:
        for file in _datafiles_names:
            shutil.move(file, _backupdir_pathname)
    except OSError:
        print("Got an exception")


def move_specified_datafiles_elsewhere(_filenames2dirnames_dict=None):
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


def return_configdict_from_config_yamlfile(_config_yamlfile_name=None):
    """Returns configuration settings as a Python dictionary
    after parsing a configuration file in YAML.

    Args:
        _config_yamlfile_name: YAML file with dictionary of configuration settings.
    """
    try:
        return return_pyobj_from_yamlstr(
            return_yamlstr_from_yamlfile(_config_yamlfile_name)
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file {repr(_config_yamlfile_name)} not found."
        )


def return_datalines_list_from_datafiles(_datafiles_names=None):
    """Returns lines from files with valid names, UTF8, with no blank lines."""
    all_datalines = []
    for datafile in _datafiles_names:
        try:
            datafile_lines = open(datafile).readlines()
        except UnicodeDecodeError:
            raise NotUTF8Error(f"{repr(datafile)} is not UTF8-encoded.")
        for line in datafile_lines:
            if not line.rstrip():
                print("Files in data directory must contain no blank lines.")
                raise BlankLinesError(f"{repr(datafile)} has blank lines.")
        all_datalines.extend(datafile_lines)

    if not all_datalines:
        raise NoDataError("No data to process!")
    return all_datalines


def return_filename2datalines_dict_after_applying_rules_to_lines(
    _ruleobjs_list=None, _datalines_list=None
):
    """Applies rules, one by one, to process aggregated datalines.

    Args:
        _ruleobjs_list: list of rule objects
        _datalines_list: list of strings (all data lines)

    Returns:
        datadict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    datadict = defaultdict(list)
    first_key_is_initialized = False

    if not _ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not _datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in datadict.
    for ruleobj in _ruleobjs_list:

        # Initialize datadict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            datadict[ruleobj.source] = _datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in datadict[ruleobj.source]:
            if is_match_to_rule_as_line(ruleobj, line):
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


def return_ruleobj_list_from_rulefile_pathnames_chain(
    _config_yamlfile=None, _rule_yamlfile_name=None, _verbose=None
):
    """Return list of rule objects from a chain (list) of rule files.

    See old version at return_ruleobj_list_from_rulefile_pathnames_chain_old

    @@@ 2019-08-15: Must be completely rewritten.
    Currently starts by recursively looking in parent
    directories for '.rules' and prepending them to list
    of rule files. If '.rules' not found in parent
    directory, stops looking.

    @@@ 2019-08-12: Change parameter _config_yamlfile to _config_pydict
    @@@ 2019-08-13: REDO as return_ruleobj_list_from_rules_list
    """

    all_rules_list = []

    config_pydict = return_pyobj_from_yamlstr(
        return_yamlstr_from_yamlfile(_yamlfile_name=CONFIG_YAMLFILE_NAME)
    )
    try:
        all_rules_list.append(config_pydict["global_rules"])
    except KeyError:
        if _verbose:
            print("No global rules found - skipping.")
    except TypeError:
        if _verbose:
            print("No global rules found - skipping.")

    rules_pylist = return_pyobj_from_yamlstr(
        return_yamlstr_from_yamlfile(_yamlfile_name=CONFIG_YAMLFILE_NAME)
    )
    try:
        all_rules_list.append(rules_pylist)
    except FileNotFoundError:
        raise RulefileNotFoundError(f"Rule file {repr(_rule_yamlfile_name)} not found.")

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


def return_ruleobj_list_from_rulefile_pathnames_chain_old(
    _config_yamlfile=None, _rule_yamlfile_name=None, _verbose=None
):
    """Return list of rule objects from a chain (list) of rule files.

    @@@ 2019-08-15: Must be completely rewritten.
    Currently starts by recursively looking in parent
    directories for '.rules' and prepending them to list
    of rule files. If '.rules' not found in parent
    directory, stops looking.

    @@@ 2019-08-12: Change parameter _config_yamlfile to _config_pydict
    @@@ 2019-08-13: REDO as return_ruleobj_list_from_rules_list
    """

    all_rules_list = []

    config_pydict = return_pyobj_from_yamlstr(
        return_yamlstr_from_yamlfile(_yamlfile_name=CONFIG_YAMLFILE_NAME)
    )
    try:
        all_rules_list.append(config_pydict["global_rules"])
    except KeyError:
        if _verbose:
            print("No global rules found - skipping.")
    except TypeError:
        if _verbose:
            print("No global rules found - skipping.")

    rules_pylist = return_pyobj_from_yamlstr(
        return_yamlstr_from_yamlfile(_yamlfile_name=CONFIG_YAMLFILE_NAME)
    )
    try:
        all_rules_list.append(rules_pylist)
    except FileNotFoundError:
        raise RulefileNotFoundError(f"Rule file {repr(_rule_yamlfile_name)} not found.")

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


def write_datafiles_from_datadict(_filename2datalines_dict=None):
    """Writes contents of filenames2datalines dictionary in which:
    * keys are names of files that will be created
    * values are contents of such files (lists of text lines)

    Note: assumes that filenames2datalines dictionary is correct:
    * filenames are valid (e.g., no pathname slashes '/')

    Args:
        _filename2datalines_dict: dictionary relating strings to lists
    """
    for (key, value) in _filename2datalines_dict.items():
        with open(key, "w", encoding="utf-8") as fout:
            fout.writelines(value)


def write_htmlfiles_from_datadict(
    _filename2datalines_dict=None, _htmldir_pathname=None, _datadir_pathname=None
):
    """Writes contents of in-memory dictionary, urlified, to disk.

    Args:
        _filenames2dirnames_dict: Python dictionary in which:
            * keys are the names of files to be written
            * values are lists of text lines.
        _htmldir_pathname: Name of HTML directory (relative to the root directory).

    Does the following:
    * creates HTML directory (if it does not already exist).
    * deletes files in htmldir (if files already exist there).
    * for each key in filenames2datalines dictionary:
      * os.path.join(_htmldir_pathname, key)
        * prepends the pathname of the HTML directory
        * appends the file extension '.html'
      * for the value (a list of text lines):
        * filters each line through return_htmlline_str_from_textstr,
          which wraps URLs in the lines with HTML angle
          brackets

    Refer to backup-related functions:
    * /Users/tbaker/github/tombaker/mklists/mklists/backups.py
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
