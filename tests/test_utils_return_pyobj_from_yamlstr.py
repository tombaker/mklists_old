"""Return Python object given a YAML string."""

import os
import pytest
from mklists.utils import return_pyobj_from_yamlstr


@pytest.mark.skip
def test_return_pyobj_from_yamlstr(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert return_pyobj_from_yamlstr(yamlfile) == result


@pytest.mark.skip
def test_return_pyobj_from_yamlstr_bad_yaml(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yaml_str = "- backups: 4\n+ verbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    with pytest.raises(SystemExit):
        return_pyobj_from_yamlstr(yamlfile)


@pytest.mark.skip
def test_return_pyobj_from_yamlstr_file_not_found(tmpdir):
    """Test with bad YAML."""
    os.chdir(tmpdir)
    yamlfile = "mklists.yml"
    with pytest.raises(SystemExit):
        return_pyobj_from_yamlstr(yamlfile)


@pytest.mark.skip
def test_read_yaml_config_yamlfile_given_good_yamlfile(tmpdir):
    """Writes string to YAML rulefile, reads back to list of lists."""
    os.chdir(tmpdir)
    lrules_yamlfile_str = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    with open("_lrules", "w") as fout:
        fout.write(lrules_yamlfile_str)
    good_pyobject = [[1, "NOW", "a", "b", 0], [1, "LATER", "a", "c", 0]]
    assert return_pyobj_from_yamlstr("_lrules") == good_pyobject


@pytest.mark.skip
def test_read_yaml_config_yamlfile_given_bad_yaml(tmpdir):
    """Trying to write bad string to YAML rulefile raises SystemExit."""
    os.chdir(tmpdir)
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    with open("_lrules_bad", "w") as fout:
        fout.write(bad_yamlstr)
    with pytest.raises(SystemExit):
        return_pyobj_from_yamlstr("_lrules_bad")
