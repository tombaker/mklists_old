"""@@@Docstring"""

import os
from mklists.utils import read_yaml_configfile_to_pyobject


def test_read_yaml_configfile_to_pyobject(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert read_yaml_configfile_to_pyobject(yamlfile) == result
