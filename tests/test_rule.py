"""Some rule module tests that use temporary directory fixture."""

import pytest
import yaml
# from mklists.rule import Rule


def test_rules(rule_yaml):
    """Test whether rule files were written to temporary directory."""
    with rule_yaml.open() as rf_y:
        yrules = yaml.load(rf_y)
    print(yrules)
    assert yrules[0][0] == 0

def test_rules2(rule_yaml):
    """Test whether rule files were written to temporary directory."""
    with rule_yaml.open() as rf_y:
        yrules = yaml.load(rf_y)
    print(yrules)
    assert yrules[0][1] == '.'
