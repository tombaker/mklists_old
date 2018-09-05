from collections import defaultdict
import re

def apply_rules_to_datalines(rules_list=None, datalines_list=None):
    """Applies rules to datalines.

    Args:
        rules_list: list of rule objects
        datalines_list: list of text lines (aggregated from data files)

    Returns:
        datalines_dict: keys are filenames, values their contents (data lines)
    """
    datalines_dict = defaultdict(list)
    initialized = False

    for rule in rules_list:
        # Sets first key in datalines_dict with value datalines_list.
        if not initialized:
            datalines_dict[rule.source] = datalines_list
            initialized = True

        for line in datalines:
            # Skip match if rule.source_matchfield is out of range.
            if rule.source_matchfield > len(line.split()):
                continue

            # Match against entire line if rule.source_matchfield is zero.
            if rule.source_matchfield == 0:
                rgx = rule.source_matchpattern
                positives = [line for line in rule.source
                             if re.search(rgx, line)]
                negatives = [line for line in rule.source
                             if not re.search(rgx, line)]
                rule.target.extend(positives)
                rule.source = negatives

            # Match field if rule.source_matchfield > 0 and within range.
            if rule.source_matchfield > 0:
                eth = rule.source_matchfield - 1
                rgx = rule.source_matchpattern
                positives = [line for line in rule.source
                             if re.search(rgx, line.split()[eth])]
                negatives = [line for line in rule.source
                             if not re.search(rgx, line.split()[eth])]
                rule.target.extend(positives)
                rule.source = negatives

            # Sort target if rule.target_sortorder greater than zero.
            if rule.target_sortorder:
                eth_sortorder = rule.target_sortorder - 1
                decorated = [(line.split()[eth_sortorder], __, line)
                             for (__, line) in enumerate(rule.target)]
                decorated.sort()
                rule.target = [line for (___, __, line) in decorated]

    return datalines_dict
