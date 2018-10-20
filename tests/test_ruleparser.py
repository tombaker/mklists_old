"""Some rule module tests that use temporary directory fixture."""

import os
import pytest
import yaml
from mklists.rule import Rule
from mklists.ruleparser import _parse_yamlrules, read_file2yaml
from mklists import VALID_FILENAME_CHARS


@pytest.mark.skip
def test_parse_yaml2rules(grules_yamlstr, lrules_yamlstr, rules_python):
    """2018-08-19: Can't believe I actually got this to work:
    * takes list of rule files
    * returns list of rule objects, as it should"""
    assert _parse_yamlrules([grules_yamlstr, lrules_yamlstr]) == rules_python

@pytest.mark.ruleparser
def test_read_file2yaml(tmpdir):
    os.chdir(tmpdir)
    content = """\
    data_folder: .
    backup_folder: .backups
    """
    # assert read_file2yaml(@@@
    assert content == content
