"""Factory to create, self-test, and lightly correct a rule object."""

import csv
import os
from pathlib import Path
from collections import defaultdict
from .ruleclass import Rule
from .booleans import dataline_is_match_to_ruleobj

from .constants import (
    ROOTDIR_RULEFILE_NAME,
    DATADIR_RULEFILE_NAME,
    CONFIG_YAMLFILE_NAME,
)
from .decorators import preserve_cwd
from .exceptions import (
    BadRuleError,
    MissingValueError,
    NoDataError,
    NoRulefileError,
    NoRulesError,
)

# pylint: disable=bad-continuation
# Black disagrees.


def return_list_of_lists_pyobj_from_rules_csvfile(csvfile=None):
    """Return lists of lists, string items stripped, from pipe-delimited CSV file."""
    csv.register_dialect("rules", delimiter="|", quoting=csv.QUOTE_NONE)
    try:
        # encoding 'utf-8-sig' for Excel files with U+FEFF
        # newline '' for MS-Windows '\r\n' line endings
        csvfile_obj = open(csvfile, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        raise NoRulefileError(f"Rule file not found.")
    except TypeError:
        raise NoRulefileError(f"No rule file specified.")

    rules_parsed_list_raw = list(csv.reader(csvfile_obj, dialect="rules"))
    rules_parsed_list = []
    for single_rule_list in rules_parsed_list_raw:
        single_rule_list_depadded = []
        if len(single_rule_list) > 4:
            for item in single_rule_list:
                single_rule_list_depadded.append(item.strip())
        if single_rule_list_depadded:
            if single_rule_list_depadded[0].isdigit():
                rules_parsed_list.append(single_rule_list_depadded[0:5])
    return rules_parsed_list


def return_names2lines_dict_from_ruleobj_and_dataline_lists(
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
            if dataline_is_match_to_ruleobj(ruleobj, line):
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


@preserve_cwd
def _return_parent_rulefile_paths(
    startdir=None,
    datadir_rulefile=DATADIR_RULEFILE_NAME,
    rootdir_rulefile=ROOTDIR_RULEFILE_NAME,
    config_yamlfile_name=CONFIG_YAMLFILE_NAME,
):
    """Return chain of rule files from root to specified data directory."""
    if not startdir:
        startdir = Path.cwd()
    os.chdir(startdir)
    root2datadir_rulefiles = []
    while datadir_rulefile in os.listdir():
        root2datadir_rulefiles.insert(0, Path.cwd().joinpath(datadir_rulefile))
        os.chdir(os.pardir)
    if config_yamlfile_name in os.listdir():
        if root2datadir_rulefiles:
            if rootdir_rulefile in os.listdir():
                root2datadir_rulefiles.insert(0, Path.cwd().joinpath(rootdir_rulefile))
    return root2datadir_rulefiles


def _return_ruleobj_list_from_pyobj(pyobj=None):
    """Return list of Rule objects from CSV string."""
    if not pyobj:
        raise NoRulesError(f"No rules list specified.")
    ruleobj_list = []
    # pyobj_filtered = [x for x in pyobj if re.match("[0-9]", x[0])]
    # for item in pyobj_filtered:
    for item in pyobj:
        try:
            if Rule(*item).is_valid():
                ruleobj_list.append(Rule(*item))
        except MissingValueError:
            print(f"Skipping badly formed rule: {item}")
        except ValueError:
            print(f"Value error.")
        except TypeError:
            raise BadRuleError(f"Rule {repr(item)} is badly formed.")
    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")
    return ruleobj_list


def return_ruleobj_list_from_rulefiles(rulefile_paths=None):
    """Return list of Rule objects from pipe-delimited CSV file."""
    one_ruleobj_list = []
    for rulefile_pathname in rulefile_paths:
        pyobj = return_list_of_lists_pyobj_from_rules_csvfile(rulefile_pathname)
        one_ruleobj_list.append(_return_ruleobj_list_from_pyobj(pyobj))
    return one_ruleobj_list
