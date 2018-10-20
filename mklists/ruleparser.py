import os
import re
import string
import sys
import pprint
import yaml
from mklists import (VALID_FILENAME_CHARS, URL_PATTERN, TIMESTAMP, MKLISTSRC,
    STARTER_GLOBALRULES, STARTER_LOCALRULES, BadFilenameError, BlankLinesError,
    DatadirHasNonFilesError, InitError, NoDataError, NoRulesError,
    NotUTF8Error, BadYamlError, BadYamlRuleError)
from mklists.rule import Rule

def get_rules(grulefile_name=None, lrulefile_name=None, 
              good_chars=None, verb=False):
    """docstring @@@"""
    rule_object_list = []
    for rulefile in grulefile_name, lrulefile_name:
        if rulefile:
            rule_object_list.extend(
                    _parse_yamlrulefile(rulefile, good_chars))
        if not rule_object_list:
            raise NoRulesError("No rules specified.")
    if verb:
        print("Rules read from rule files:")
        pprint.pprint(rule_object_list)
    return rule_object_list

def _parse_yamlrules(rulefile, good_chars=VALID_FILENAME_CHARS):
    """Returns list of rule objects from parsing a YAML-format rule file."""
    parsed_yaml = _parse_yaml(rulefile)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    for rule_object in rule_objects_list:
        rule_object.is_valid(good_chars)
    return rule_objects_list

def _parse_yaml(rulefile):
    """Returns unvalidated list of split-out rule lines.
    
    Args:
        rulefile: a file of rules in YAML format

    Raises:
        ParserError??
    """
    list_parsed_from_yaml = []
    try:
        with open(rulefile) as rfile:
            list_parsed_from_yaml.extend(yaml.load(rfile))
    #except ParserError: # can this happen here?
    #    raise BadYamlError(f"YAML format of {rulefile} does not parse.")
    except FileNotFoundError:
        print(f"{repr(rulefile)} not found - skipping.")
    return list_parsed_from_yaml

def _create_list_of_rule_objects(rule_list_from_yaml: list = None):
    """Returns list of rule objects.

    Args:
        rule_list_from_yaml: list of unvalidated split-out rule lines.
    """
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRuleError(f"{item} is badly formed.")
    return list_of_rule_objects

