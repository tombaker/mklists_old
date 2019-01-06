"""@@@Docstring"""

import os
import pytest
from mklists.utils import write_yamlstr_to_yamlfile, return_pydict_from_yaml_configfile


def test_return_pydict_from_yaml_configfile(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert return_pydict_from_yaml_configfile(yamlfile) == result


def test_return_pydict_from_yaml_configfile_bad_yaml(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yaml_str = "- backups: 4\n+ verbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    with pytest.raises(SystemExit):
        return_pydict_from_yaml_configfile(yamlfile)


def test_return_pydict_from_yaml_configfile_file_not_found(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yamlfile = "mklists.yml"
    with pytest.raises(SystemExit):
        return_pydict_from_yaml_configfile(yamlfile)


def test_read_yaml_configfile_given_good_yamlfile(tmpdir):
    """Writes string to YAML rulefile, reads back to list of lists."""
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules", lrules_yamlstr)
    good_pyobject = [[1, "NOW", "a", "b", 0], [1, "LATER", "a", "c", 0]]
    assert return_pydict_from_yaml_configfile("_lrules") == good_pyobject


def test_read_yaml_configfile_given_bad_yaml(tmpdir):
    """Trying to write bad string to YAML rulefile raises SystemExit."""
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    write_yamlstr_to_yamlfile("_lrules_bad", bad_yamlstr)
    with pytest.raises(SystemExit):
        return_pydict_from_yaml_configfile("_lrules_bad")
