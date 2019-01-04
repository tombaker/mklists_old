"""@@@Docstring"""

import os
from mklists.utils import read_yaml_configfile_to_pyobject, write_yamlstr_to_yamlfile


def test_write_yamlstr_to_yamlfile(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    write_yamlstr_to_yamlfile(yamlfile, yaml_str)
    result = {"backups": 3, "verbose": False}
    assert read_yaml_configfile_to_pyobject(yamlfile) == result


def test_write_yamlstr_to_yamlfile_too(tmpdir):
    """Writes string to YAML rulefile, reads it back to string."""
    os.chdir(tmpdir)
    lr_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules", lr_yamlstr)
    assert lr_yamlstr == open("_lrules").read()
