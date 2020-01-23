"""Writes YAML configuration file, 'mklists.yml', to repo root directory."""

import os
import pytest
from mklists.constants import CONFIG_YAMLFILE_CONTENT, CONFIG_YAMLFILE_NAME
from mklists.voids import write_config_yamlfile


def test_write_config_yamlfile(tmpdir):
    """Write contents of CONFIG_YAMLFILE_CONTENT constant to 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile()
    assert open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_CONTENT


def test_write_config_yamlfile_not_if_already_exists(tmpdir):
    os.chdir(tmpdir)
    tmpdir.join(CONFIG_YAMLFILE_NAME).write("Config stuff")
    with pytest.raises(SystemExit):
        write_config_yamlfile()