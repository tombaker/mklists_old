"""Apply rules to process datalines."""

from collections import defaultdict
from .exceptions import (
    BadYamlRuleError,
    BlankLinesError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
    RulefileNotFoundError,
)
from .constants import RULE_YAMLFILE_NAME, CONFIG_YAMLFILE_NAME
from .rules import Rule
from .utils import return_pyobj_from_config_yamlfile, is_line_match_to_rule


def return_datalines_dict_after_applying_rules(ruleobj_list=None, dataline_list=None):
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


def return_datalines_list_from_datafiles(listfile_names=None):
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


def return_ruleobj_list_from_rule_yamlfiles(
    config_yamlfile=CONFIG_YAMLFILE_NAME, rule_yamlfile=RULE_YAMLFILE_NAME, verbose=True
):
    """Return list of rule objects from rule files.

    2019-07-21: Starts by recursively looking in parent
    directories for '.rules' and prepending them to list
    of rule files. If '.rules' not found in parent
    directory, stops looking.
    """

    all_rules_list = []

    config_pydict = return_pyobj_from_config_yamlfile(config_yamlfile)
    try:
        all_rules_list.append(config_pydict["global_rules"])
    except KeyError:
        if verbose:
            print("No global rules found - skipping.")
    except TypeError:
        if verbose:
            print("No global rules found - skipping.")

    rules_pylist = return_pyobj_from_config_yamlfile(rule_yamlfile)
    try:
        all_rules_list.append(rules_pylist)
    except FileNotFoundError:
        raise RulefileNotFoundError(f"Rule file {repr(rule_yamlfile)} was not found.")

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


def write_datafiles_from_datadict(datadict=None):
    """
    -- Write out contents of datadict to working directory:
       -- datadict keys are names of files.
       -- datadict values are contents of files.
    """
    for (key, value) in datadict.items():
        with open(key, "w", encoding="utf-8") as fout:
            fout.writelines(value)
