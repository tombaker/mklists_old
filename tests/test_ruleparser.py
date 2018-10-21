"""Some rule module tests that use temporary directory fixture."""

import os
import pytest
import yaml
from mklists.rule import Rule
from mklists.ruleparser import _parse_yamlrules, read_file2yaml
from mklists import VALID_FILENAME_CHARS


@pytest.mark.skip
def test_parse_yaml2rules(grules_yamlstr, lrules_yamlstr, rules_python):
    assert _parse_yamlrules([grules_yamlstr, lrules_yamlstr]) == rules_python

@pytest.mark.skip
def test_read_file2yaml(rules_yamlfile, lrules_yamlstr):
    assert read_file2yaml(rules_yamlfile) == lrules_yamlstr

@pytest.mark.ruleparser
def test_parse_file2yaml(rules_yamlfile):
    expected = yaml.load(open(rules_yamlfile, 'r'))
    assert read_file2yaml(rules_yamlfile) == expected

@pytest.mark.ruleparser
def test_parse_file2yaml_raise_scannererror(rules_yamlfile_bad_scannererror):
    with pytest.raises(SystemExit):
        read_file2yaml(rules_yamlfile_bad_scannererror)
