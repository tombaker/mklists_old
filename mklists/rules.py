"""Rules docstring

Issues: make sure an empty .globalrules file would return an empty list
"""

import yaml
from mklists.rule import Rule
from mklists import (
    VALID_FILENAME_CHARS,
    RuleFileNotFoundError,
    BadYamlError, 
    BadYamlRuleError)


# should this be *rulefiles instead? - not need to be passed as list?
def parse_rules(rulefiles, good_chars=VALID_FILENAME_CHARS):
    """Returns list of rule objects by parsing list of rule files."""
    parsed_yaml = _parse_yaml(rulefiles)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    for rule in rule_objects_list:
        rule.is_valid(good_chars)
    return rule_objects_list

def _parse_yaml(list_of_rulefiles):
    """Returns pre-validated list of rules parsed from YAML files"""
    list_parsed_from_yaml = []
    for rulefile in list_of_rulefiles:
        try:
            with open(rulefile) as rfile:
                list_parsed_from_yaml.extend(yaml.load(rfile))
        except ParserError:
            raise BadYamlError(f"YAML format of {rulefile} does not parse.")
        except FileNotFoundError:
            raise RuleFileNotFoundError(f"{repr(rulefile)} not found.")
    return list_parsed_from_yaml

def _create_list_of_rule_objects(rule_list_from_yaml: list = None):
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRuleError(f"{item} is badly formed.")
    return list_of_rule_objects

