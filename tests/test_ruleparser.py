"""Some rule module tests that use temporary directory fixture."""

import os
import pytest
import yaml
from mklists.rule import Rule
from mklists import VALID_FILENAME_CHARS
from mklists.readwrite import (write_yamlstr_to_yamlfile, 
    read_yamlfile_return_pyobject)


@pytest.mark.yaml
def test_write_yamlstr(tmpdir):
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules', lrules_yamlstr)
    some_yamlstr = open('_lrules').read()
    assert lrules_yamlstr == some_yamlstr

@pytest.mark.yaml
def test_read_good_yamlfile(tmpdir):
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules', lrules_yamlstr)
    pyobject = read_yamlfile_return_pyobject('_lrules')
    good_pyobject = [[1, 'NOW', 'a', 'b', 0], [1, 'LATER', 'a', 'c', 0]]
    assert pyobject == good_pyobject

@pytest.mark.yaml
def test_read_bad_yamlfile(tmpdir):
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile('_lrules_bad', bad_yamlstr)
    with pytest.raises(SystemExit):
        read_yamlfile_return_pyobject('_lrules_bad')

