"""Return contents (presumably a YAML string) from file that is supposed to have YAML."""

import io
import os
import pytest
from mklists.exceptions import YamlFileNotFoundError
from mklists.run import read_yamlfile_return_yamlstr

CONFIG_YAMLFILE_NAME = "mklists.yml"


def test_read_yamlfile_return_yamlstr(tmpdir):
    """Writes YAML string to YAML file, then reads file back to a YAML string."""
    os.chdir(tmpdir)
    yamlstr = "backups: 3\nverbose: false"
    default_yamlfile_name = "mklists.yml"
    with open(default_yamlfile_name, "w") as fout:
        fout.write(yamlstr)
    assert io.open(default_yamlfile_name).read() == yamlstr
    assert read_yamlfile_return_yamlstr(default_yamlfile_name) == yamlstr


def test_read_yamlfile_return_yamlstr_notfound(tmpdir):
    """Tries to read a non-existent YAML file: SystemExit with error message"""
    os.chdir(tmpdir)
    default_yamlfile_name = "mklists.yml"
    with pytest.raises(SystemExit):
        read_yamlfile_return_yamlstr(default_yamlfile_name)


def test_read_yamlfile_return_yamlstr_notfound_extra(tmpdir):
    """Tries to read a non-existent YAML file: YamlFileNotFoundError with error message"""
    os.chdir(tmpdir)
    default_yamlfile_name = "mklists.yml"
    with pytest.raises(YamlFileNotFoundError):
        read_yamlfile_return_yamlstr(default_yamlfile_name)
