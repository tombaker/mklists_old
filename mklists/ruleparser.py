import pprint
import yaml
from mklists import (VALID_FILENAME_CHARS, 
                     NoRulesError, 
                     BadYamlRuleError,
                     BadYamlError)
from mklists.rule import Rule

def parse_file2yaml(yamlfile_name: str):
    """Returns Python object parsed from given YAML file."""
    try:
        x = yaml.load(open(yamlfile_name, 'r'))
    except ScannerError:
        raise BadYamlError(f"YAML format of {yamlfile_name} does not parse.")

def read_file2yaml(yamlfile_name: str):
    """Returns Python object parsed from given YAML file."""
    try:
        return yaml.load(open(yamlfile_name, 'r'))
    except:
        BadYamlError(f"YAML format of {yamlfile_name} does not parse.")

def get_rules(grulefile_name=None, lrulefile_name=None, 
              good_chars=None, verbose=False):
    rule_object_list = []
    for rulefile in grulefile_name, lrulefile_name:
        if rulefile:
            rule_object_list.extend(
                    _parse_yamlrulefile(rulefile, good_chars))
        if not rule_object_list:
            raise NoRulesError("No rules specified.")
    if verbose:
        print("Rules read from rule files:")
        pprint.pprint(rule_object_list)
    return rule_object_list

def _parse_yamlrules(rulefile, good_chars=VALID_FILENAME_CHARS):
    parsed_yaml = _parse_yaml(rulefile)
    rule_objects_list = _create_list_of_rule_objects(parsed_yaml)
    for rule_object in rule_objects_list:
        rule_object.is_valid(good_chars)
    return rule_objects_list

def _parse_yaml(rulefile):
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
    list_of_rule_objects = []
    for item in rule_list_from_yaml:
        try:
            list_of_rule_objects.append(Rule(*item))
        except TypeError:
            raise BadYamlRuleError(f"{item} is badly formed.")
    return list_of_rule_objects

