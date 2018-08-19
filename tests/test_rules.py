"""Some rule module tests that use temporary directory fixture."""

import pytest
import yaml
from mklists.rule import Rule
from mklists.rules import parse_yamlfiles_to_ruleslist


def test_rules(rule_yaml):
    """Test whether rule files were written to temporary directory."""
    with open(rule_yaml) as rf_y:
        yrules = yaml.load(rf_y)
    print(yrules)
    print(type(rule_yaml))
    assert yrules[0][0] == 0

def test_parse_yaml2rules(rule_global_yaml, rule_yaml, rules_python):
    """2018-08-19: Can't believe I actually got this to work:
    * takes list of rule files
    * returns list of rule objects, as it should"""
    assert parse_yamlfiles_to_ruleslist([rule_global_yaml, rule_yaml]) == rules_python

