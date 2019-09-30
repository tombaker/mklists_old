"""Return Python object given a YAML string."""

import os
import pytest
from mklists.utils import return_yamlobj_from_yamlstr


def test_read_return_yamlobj_from_yamlstr_given_good_yamlstr(tmpdir):
    """Returns Python object given a YAML string."""
    yamlstr = "backups: 3\nverbose: false"
    result = {"backups": 3, "verbose": False}
    assert return_yamlobj_from_yamlstr(_yamlstr=yamlstr) == result


def test_read_return_yamlobj_from_yamlstr_given_another_good_yamlstr(tmpdir):
    """Returns Python object given a YAML string."""
    yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    result = [[1, "NOW", "a", "b", 0], [1, "LATER", "a", "c", 0]]
    assert return_yamlobj_from_yamlstr(_yamlstr=yamlstr) == result


def test_return_yamlobj_from_yamlstr_given_bad_yaml(tmpdir):
    """Raises SystemExit when given bad YAML."""
    bad_yamlstr = "- backups: 4\n+ verbose: false"
    with pytest.raises(SystemExit):
        return_yamlobj_from_yamlstr(_yamlstr=bad_yamlstr)


def test_read_yaml_config_yamlfile_given_more_bad_yaml(tmpdir):
    """Raises SystemExit when given bad YAML."""
    bad_yamlstr = """
    - [1, 'NOW', a, b, 0]
    + [1, 'LATER', a, c, 0]"""
    with pytest.raises(SystemExit):
        return_yamlobj_from_yamlstr(_yamlstr=bad_yamlstr)
