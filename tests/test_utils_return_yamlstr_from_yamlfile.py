"""Return contents (presumably a YAML string) from file that is supposed to have YAML."""

import io
import os
import pytest
from mklists.constants import CONFIG_YAMLFILE_NAME
from mklists.exceptions import YamlFileNotFoundError
from mklists.utils import return_yamlstr_from_yamlfile


def test_return_yamlstr_from_yamlfile(tmpdir):
    """Writes YAML string to YAML file,
    then reads file back to a YAML string."""
    os.chdir(tmpdir)
    yaml_str = "backups: 3\nverbose: false"
    yamlfile_name = "mklists.yml"
    with open(yamlfile_name, "w") as fout:
        fout.write(yaml_str)
    assert io.open(yamlfile_name).read() == yaml_str
    assert return_yamlstr_from_yamlfile(_yamlfile_name=yamlfile_name) == yaml_str


def test_return_yamlstr_from_yamlfile_notfound(tmpdir):
    """Tries to read a non-existent YAML file and exits with error message."""
    os.chdir(tmpdir)
    with pytest.raises(YamlFileNotFoundError):
        return_yamlstr_from_yamlfile(_yamlfile_name=CONFIG_YAMLFILE_NAME)
