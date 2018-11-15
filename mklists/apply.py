"""Apply rules to process datalines."""

import re
from collections import defaultdict
from mklists import NoDataError, NoRulesError


def apply_rules_to_datalines(ruleobjs_list=None, datalines_list=None):
    """Applies rules, one by one, to process an aggregated list of datalines.

    Args:
        ruleobjs_list: list of rule objects
        datalines_list: list of strings (all data lines)

    Returns:
        mklists_dict - dictionary where:
        * key: always a string that is valid as a filename
        * value: always a list of (part of the) data lines
    """
    mklists_dict = defaultdict(list)
    first_key_is_initialized = False

    if not ruleobjs_list:
        raise NoRulesError("No rules specified.")

    if not datalines_list:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in mklists_dict.
    for ruleobj in ruleobjs_list:

        # Initialize mklists_dict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            mklists_dict[ruleobj.source] = datalines_list
            first_key_is_initialized = True

        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in mklists_dict[ruleobj.source]:
            if _line_matches(ruleobj, line):
                mklists_dict[ruleobj.target].extend([line])
                mklists_dict[ruleobj.source].remove(line)

        # Sort 'ruleobj.target' lines by field if sortorder was specified.
        if ruleobj.target_sortorder:
            eth_sortorder = ruleobj.target_sortorder - 1
            decorated = [
                (line.split()[eth_sortorder], __, line)
                for (__, line) in enumerate(mklists_dict[ruleobj.target])
            ]
            decorated.sort()
            mklists_dict[ruleobj.target] = [
                line for (___, __, line) in decorated
            ]

    return dict(mklists_dict)


def _line_matches(given_rule=None, given_line=None):
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
