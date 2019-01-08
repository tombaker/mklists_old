"""@@@Docstring"""

import os
from mklists.utils import return_pyobj_from_yamlfile, write_yamlstr_to_yamlfile


def test_write_yamlstr_to_yamlfile(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    write_yamlstr_to_yamlfile(yaml_str, yamlfile)
    result = {"backups": 3, "verbose": False}
    assert return_pyobj_from_yamlfile(yamlfile) == result


def test_write_yamlstr_to_yamlfile_too(tmpdir):
    """Writes string to YAML rulefile, reads it back to string."""
    os.chdir(tmpdir)
    lr_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile(lr_yamlstr, "_lrules")
    assert lr_yamlstr == open("_lrules").read()
