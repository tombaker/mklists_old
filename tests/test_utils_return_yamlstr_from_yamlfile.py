"""Return contents (presumably a YAML string) from file that is supposed to have YAML."""

import io
import os
import pytest
from mklists.constants import CONFIG_YAMLFILE_NAME
from mklists.exceptions import YamlFileNotFoundError
from mklists.utils import return_yamlstr_from_yamlfile


def test_return_yamlstr_from_yamlfile(tmpdir):
    """Writes YAML string to YAML file, then reads file back to a YAML string."""
    os.chdir(tmpdir)
    yamlstr = "backups: 3\nverbose: false"
    yamlfile_name = "mklists.yml"
    with open(yamlfile_name, "w") as fout:
        fout.write(yamlstr)
    assert io.open(yamlfile_name).read() == yamlstr
    assert return_yamlstr_from_yamlfile(_yamlfile_name=yamlfile_name) == yamlstr


def test_return_yamlstr_from_yamlfile_notfound(tmpdir):
    """Tries to read a non-existent YAML file: SystemExit with error message"""
    os.chdir(tmpdir)
    yamlfile_name = "mklists.yml"
    with pytest.raises(SystemExit):
        return_yamlstr_from_yamlfile(_yamlfile_name=yamlfile_name)


def test_return_yamlstr_from_yamlfile_notfound_extra(tmpdir):
    """Tries to read a non-existent YAML file: YamlFileNotFoundError with error message"""
    os.chdir(tmpdir)
    yamlfile_name = "mklists.yml"
    with pytest.raises(YamlFileNotFoundError):
        return_yamlstr_from_yamlfile(_yamlfile_name=yamlfile_name)
