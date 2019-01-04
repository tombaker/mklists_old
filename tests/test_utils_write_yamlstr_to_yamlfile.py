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
