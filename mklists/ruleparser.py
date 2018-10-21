import pprint
import yaml
from mklists import (VALID_FILENAME_CHARS, 
                     NoRulesError, 
                     BadYamlRuleError,
                     BadYamlError)
from mklists.rule import Rule

# for each rulefile:
# 
# def read_yamlfile_return_pyobj(yamlfile_name)
#     """Returns Python object (eg, list or dict) from file in YAML format."""
# 
#     return yaml.load(open(yamlfile_name))
# 
#     yaml.load(open(yamlfile_name))
#     rule_object_list.extend(some_list)
#     rule_object_list.append(some_string)
# 
#     TypeError:
#     FileNotFoundError:
# 
#     BadYamlError(f"YAML format of {yamlfile_name} does not parse.")
#     BadYamlRuleError(f"{item} is badly formed.")
#     NoRulesError("No rules specified.")
# 
# grulesfile_name # filename, a string, for global rules file
# grulesfile_obj  # Python object, returned by open(file), for global rules file
# lrulesfile_name # filename, a string, for local rules file
# lrulesfile_obj  # Python object, returned by open(file), for local rules file
# rule_obj        # Rule() instance
# ruleparsed_str  # string, representing a rule, split into fields
# ruleraw_str     # string, representing a rule, edited by a user (eg part of grulesfile
# yaml2dict_obj   # Python object, returned by yaml.load, for a dictionary
# yaml2list_obj   # Python object, returned by yaml.load, for a list
# yamlfile_name   # filename, a string, for file in YAML format
# yamlfile_obj    # Python object, returned by open(file), for file in YAML format
