"""Rules docstring"""

import yaml
from mklists.rule import Rule
from mklists import VALID_FILENAME_CHARS


def parse_rules(rulefiles, good_chars=VALID_FILENAME_CHARS, bad_pats=None):
    """docstring
        bad_pats: patterns (regular expressions) for invalid filenames
    """
    parsed_yaml = _parse_yaml(rulefiles)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    _rule_objects_are_valid(rule_objects_list) # bad_pats?
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

    # test for bad YAML here?
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRule(f"{item} is badly formed.")

    return list_of_rule_objects

def _rule_objects_are_valid(list_of_rule_objects): # add bad_pats?
    for rule in list_of_rule_objects:
        if rule.is_valid(): # add bad_pats?
            pass

    return True


class RulesErrors(SystemExit):
    """Category of exceptions related to sets or rules."""


class RuleFileNotFoundError(RulesErrors):
    """Rule file not found or not accessible."""


class BadYamlRule(RulesErrors):
    """Rule is badly formed in YAML source."""


DEFAULT_RULE_FILE = """\
- [0,  '.',         lines,         todo.txt,   0]  # notes...
- [1,  'NOW',       todo.txt,      now.txt,    0]  # notes...
- [1,  'LATER',     todo.txt,      later.txt,  0]  # notes...
"""
