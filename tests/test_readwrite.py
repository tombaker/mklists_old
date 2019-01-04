"""for readwrite.py"""

import os
import pytest
from mklists.utils import write_yamlstr_to_yamlfile, read_yaml_configfile_to_pyobject


@pytest.mark.yaml
def test_write_yamlstr(tmpdir):
    """Writes string to YAML rulefile, reads it back to string."""
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules", lrules_yamlstr)
    some_yamlstr = open("_lrules").read()
    assert lrules_yamlstr == some_yamlstr


@pytest.mark.yaml
def test_read_good_yamlfile(tmpdir):
    """Writes string to YAML rulefile, reads back to list of lists."""
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules", lrules_yamlstr)
    pyobject = read_yaml_configfile_to_pyobject("_lrules")
    good_pyobject = [[1, "NOW", "a", "b", 0], [1, "LATER", "a", "c", 0]]
    assert pyobject == good_pyobject


@pytest.mark.yaml
def test_read_bad_yamlfile(tmpdir):
    """Trying to write bad string to YAML rulefile raises SystemExit."""
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules_bad", bad_yamlstr)
    with pytest.raises(SystemExit):
        read_yaml_configfile_to_pyobject("_lrules_bad")
