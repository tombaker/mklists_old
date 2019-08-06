"""Apply rules to process datalines."""

from collections import defaultdict
from .booleans import is_line_match_to_rule
from .exceptions import (
    BadYamlRuleError,
    BlankLinesError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RulefileNotFoundError,
)
from .rules import Rule
from .utils import _return_pyobj_from_yamlfile

# import re
# import yaml
# from .constants import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
# from .constants import URL_PATTERN_REGEX
#     BadYamlError,
#     ConfigFileNotFoundError,


def return_configdict_from_config_yamlfile():
    pass


def return_filename2datalines_dict_after_applying_rules(
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


def return_ruleobj_list_from_rule_yamlfiles(
    config_yamlfile=None, _rule_yamlfile_name=None, _verbose=None
):
    """Return list of rule objects from rule files.

    2019-07-21: Starts by recursively looking in parent
    directories for '.rules' and prepending them to list
    of rule files. If '.rules' not found in parent
    directory, stops looking.
    """

    all_rules_list = []

    config_pydict = _return_pyobj_from_yamlfile(config_yamlfile)
    try:
        all_rules_list.append(config_pydict["global_rules"])
    except KeyError:
        if _verbose:
            print("No global rules found - skipping.")
    except TypeError:
        if _verbose:
            print("No global rules found - skipping.")

    rules_pylist = _return_pyobj_from_yamlfile(_rule_yamlfile_name)
    try:
        all_rules_list.append(rules_pylist)
    except FileNotFoundError:
        raise RulefileNotFoundError(
            f"Rule file {repr(_rule_yamlfile_name)} was not found."
        )

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


def relocate_specified_datafiles_elsewhere(_filename2dirname_dict=None):
    """Args: _filename2dirname_dict: filename (key) and destination directory (value)
    See /Users/tbaker/github/tombaker/mklists/tests/test_run_relocate_specified_datafiles_elsewhere
    """


def write_datafiles_from_datadict(_filename2datalines_dict=None):
    """
    -- Write out contents of _filename2datalines_dict to working directory:
       -- _filename2datalines_dict keys are names of files.
       -- _filename2datalines_dict values are contents of files.
    """
    for (key, value) in _filename2datalines_dict.items():
        with open(key, "w", encoding="utf-8") as fout:
            fout.writelines(value)


def write_htmlfiles_from_datadict(_filename2datalines_dict=None, _verbose=False):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_run_write_htmlfiles_from_datadict_LATER.py
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of _filename2datalines_dict to working directory:
       -- _filename2datalines_dict keys are filenames.
          -- for each filename, add file extension '.html'
       -- _filename2datalines_dict values are contents of files.
          -- filter each line through _return_htmlstr_from_textstr.
    """
