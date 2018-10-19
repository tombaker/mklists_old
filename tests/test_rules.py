"""Some rule module tests that use temporary directory fixture."""

import pytest
import yaml
from mklists.rule import Rule
from mklists.readwrite import _parse_yamlrules


@pytest.mark.rule
def test_parse_yaml2rules(rule_global_yaml, rule_yaml, rules_python):
    """2018-08-19: Can't believe I actually got this to work:
    * takes list of rule files
    * returns list of rule objects, as it should"""
    assert _parse_yamlrules([rule_global_yaml, rule_yaml]) == rules_python

