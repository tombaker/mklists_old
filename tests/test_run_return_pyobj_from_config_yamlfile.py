"""return_pyobj_from_yamlfile():
* is called by run:return_ruleobj_list_from_rule_yamlfiles()"""

import os
import pytest
import yaml
from mklists.run import _return_pyobj_from_yamlfile


def test_return_pyobj_from_yamlfile(tmpdir):
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert _return_pyobj_from_yamlfile(yamlfile) == result


def test_return_pyobj_from_yamlfile_bad_yaml(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yaml_str = "- backups: 4\n+ verbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    with pytest.raises(SystemExit):
        _return_pyobj_from_yamlfile(yamlfile)


def test_return_pyobj_from_yamlfile_file_not_found(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yamlfile = "mklists.yml"
    with pytest.raises(SystemExit):
        _return_pyobj_from_yamlfile(yamlfile)


def test_read_yaml_config_yamlfile_given_good_yamlfile(tmpdir):
    """Writes string to YAML rulefile, reads back to list of lists."""
    os.chdir(tmpdir)
    lrules_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    with open("_lrules", "w") as fout:
        fout.write(lrules_yamlstr)
    good_pyobject = [[1, "NOW", "a", "b", 0], [1, "LATER", "a", "c", 0]]
    assert _return_pyobj_from_yamlfile("_lrules") == good_pyobject


def test_read_yaml_config_yamlfile_given_bad_yaml(tmpdir):
    """Trying to write bad string to YAML rulefile raises SystemExit."""
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    with open("_lrules_bad", "w") as fout:
        fout.write(bad_yamlstr)
    with pytest.raises(SystemExit):
        _return_pyobj_from_yamlfile("_lrules_bad")
