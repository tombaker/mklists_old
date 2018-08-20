"""Shuffle module docstring"""

from collections import defaultdict
import re

def apply_rules_to_datalines(rules, datalines):
    """
    Args:
        rules: list of (validated) rule objects
        datalines: all datalines (list)

    Initializes dictionary structure where:
    * values hold (changing) portions of 'datalines'
    * keys are filenames to which values will be written
    """

    datalines_dict = defaultdict(list)
    initialized = False

    for rule in rules:

        if not initialized:
            datalines_dict[rule.source] = rule.source
            initialized = True

        for line in datalines:
            # skip match if rule.source_matchfield out of range
            if rule.source_matchfield > len(line.split()):
                continue

            # match against entire line if rule.source_matchfield is zero
            if rule.source_matchfield == 0:
                rgx = rule.source_matchpattern
                positives = [line for line in rule.source
                             if re.search(rgx, line)]
                negatives = [line for line in rule.source
                             if not re.search(rgx, line)]
                rule.target.extend(positives)
                rule.source = negatives

            # match field if rule.source_matchfield > 0 and within range
            if rule.source_matchfield > 0:
                eth = rule.source_matchfield - 1
                rgx = rule.source_matchpattern
                positives = [line for line in rule.source
                             if re.search(rgx, line.split()[eth])]
                negatives = [line for line in rule.source
                             if not re.search(rgx, line.split()[eth])]
                rule.target.extend(positives)
                rule.source = negatives

            # sort target if rule.target_sortorder greater than zero
            if rule.target_sortorder:
                eth_sortorder = rule.target_sortorder - 1
                decorated = [(line.split()[eth_sortorder], __, line)
                             for __, line in enumerate(rule.target)]
                decorated.sort()
                rule.target = [line for ___, __, line in decorated]

        return all

    return datalines_dict

