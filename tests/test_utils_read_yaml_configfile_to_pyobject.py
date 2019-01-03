"""@@@Docstring"""

import os
import pytest
from mklists.utils import read_yaml_configfile_to_pyobject


def test_read_yaml_configfile_to_pyobject(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert read_yaml_configfile_to_pyobject(yamlfile) == result


def test_read_yaml_configfile_to_pyobject_bad_yaml(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yaml_str = "- backups: 4\n+ verbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    with pytest.raises(SystemExit):
        read_yaml_configfile_to_pyobject(yamlfile)


def test_read_yaml_configfile_to_pyobject_file_not_found(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yamlfile = "mklists.yml"
    with pytest.raises(SystemExit):
        read_yaml_configfile_to_pyobject(yamlfile)
