"""Apply rules to process datalines."""

import re
import yaml
from collections import defaultdict
from mklists import (
    ConfigFileNotFoundError,
    BadYamlError,
    BlankLinesError,
    NoDataError,
    NoRulesError,
    NotUTF8Error,
)


def get_datalines_from_listfiles(listfile_names: list):
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


def _get_pyobj_from_yamlfile(yamlfile_name):
    """Returns Python object parsed from given YAML-format file."""
    try:
        yamlstr = open(yamlfile_name).read()
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"YAML file {repr(yamlfile_name)} not found.")

    try:
        return yaml.load(yamlstr)
    except yaml.YAMLError:
        raise BadYamlError(f"Badly formatted YAML in {repr(yamlfile_name)}.")


def apply_rules_to_datalines(ruleobjs_list=None, datalines_list=None):
    """Applies rules, one by one, to process an aggregated list of datalines.

    Args:
        ruleobjs_list: list of rule objects
        datalines_list: list of strings (all data lines)

    Returns:
        data_dict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    data_dict = defaultdict(list)
    first_key_is_initialized = False

    if not ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in data_dict.
    for ruleobj in ruleobjs_list:

        # Initialize data_dict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            data_dict[ruleobj.source] = datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in data_dict[ruleobj.source]:
            if _line_matches_rule(ruleobj, line):
                data_dict[ruleobj.target].extend([line])
                data_dict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(data_dict[ruleobj.target])
            ]
            decorated.sort()
            data_dict[ruleobj.target] = [line for (___, __, line) in decorated]

    return dict(data_dict)


def _line_matches_rule(given_rule=None, given_line=None):
    """Returns True if data line matches pattern specified in given rule."""

    # Line does not match if given field greater than number of fields in line.
    if given_rule.source_matchfield > len(given_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_rule.source_matchfield == 0:
        if re.search(given_rule.source_matchpattern, given_line):
            return True

    # Line matches if pattern is found in given field.
    if given_rule.source_matchfield > 0:
        eth = given_rule.source_matchfield - 1
        if re.search(given_rule.source_matchpattern, given_line.split()[eth]):
            return True

    return False


def write_mkldict_to_htmlfiles(data_dict={}, verbose=False):
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
    print(f"* Move files outside listdir as per ['files2dirs'].")


def write_mkldict_to_listfiles(data_dict=None, verbose=False):
    """If 'backup' is ON, move existing files from working to backup directory.
    If 'backup' is OFF, DELETE existing files in working directory.
    Write data_dict to working directory:
    -- data_dict keys are names of files.
    -- data_dict values are contents of files."""
