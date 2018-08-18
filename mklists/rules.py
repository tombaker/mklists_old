"""Rules docstring"""

from collections import defaultdict
import re
import yaml
from mklists.rule import Rule

def parse_yamlfiles_to_ruleslist(rulefiles):
    """docstring"""
    parsed_yaml = _parse_yaml(rulefiles)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    _rule_objects_are_valid(rule_objects_list)
    return rule_objects_list

def _parse_yaml(rulefiles):
    """Issue: what if rulefiles is a string?  Should be permitted."""
    list_parsed_from_yaml = []
    for rulefile in rulefiles:
        try:
            with open(rulefile) as rfile:
                list_parsed_from_yaml.extend(yaml.load(rfile))
        except FileNotFoundError:
            print(f"Expected rule files: {rulefiles}.")
            raise RuleFileNotFoundError(f"{repr(rulefile)} not found.")

    return list_parsed_from_yaml

def _create_list_of_rule_objects(rule_list_from_yaml: list = None):
    """docstring"""
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRule(f"{item} is badly formed.")

    return list_of_rule_objects

def _rule_objects_are_valid(list_of_rule_objects):
    source_list_initialized = False
    source_list = []

    for rule in list_of_rule_objects:
        if not source_list_initialized:
            source_list.append(rule.source)
            source_list.append(rule.target)
            source_list_initialized = True
        if rule.source not in source_list:
            raise SourceNotPrecedentedError("source has no precedent")
        else:
            source_list.append(rule.target)

        if rule.is_valid():
            pass

        return True

def apply_rules_to_datalines(rules, datalines):
    """
    Args:
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


class RulesErrors(SystemExit):
    """Category of exceptions related to sets or rules."""


class RuleFileNotFoundError(RulesErrors):
    """Rule file not found or not accessible."""


class SourceNotPrecedentedError(RulesErrors):
    """Source has not been previously initialized."""


class BadYamlRule(RulesErrors):
    """Rule is badly formed in YAML source."""
