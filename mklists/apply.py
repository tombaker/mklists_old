"""Generates filename-to-datalines dictionary by matching lines to rules."""

from collections import defaultdict
from .booleans import dataline_matches_ruleobj
from .exceptions import NoDataError, NoRulesError


def apply_rules_to_datalines(ruleobjs=None, datalines=None):
    """Applies rules, one by one, to process aggregated datalines."""
    datadict = defaultdict(list)
    first_key_is_initialized = False
    if not ruleobjs:
        raise NoRulesError("No rules specified.")
    if not datalines:
        raise NoDataError("No data specified.")

    # Evaluate rules, one-by-one, to process entries in datadict.
    for ruleobj in ruleobjs:
        # Initialize datadict with first rule.
        #    key: valid filename (from 'source' field of first ruleobj)
        #    value: list of all data lines
        if not first_key_is_initialized:
            datadict[ruleobj.source] = datalines
            first_key_is_initialized = True
        # Match lines in 'ruleobj.source' against 'rulesobj.regex'.
        #    append matching lines to value of 'ruleobj.target'
        #    remove matching lines from value of 'ruleobj.source'
        for line in datadict[ruleobj.source]:
            if dataline_matches_ruleobj(ruleobj, line):
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
