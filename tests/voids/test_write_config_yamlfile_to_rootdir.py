"""Writes YAML configuration file, 'mklists.yml', to repo root directory."""

import os
import pytest
from pathlib import Path
from mklists.constants import CONFIG_YAMLFILE_CONTENT, CONFIG_YAMLFILE_NAME
from mklists.voids import write_config_yamlfile


def test_write_config_yamlfile(tmp_path):
    """Write contents of CONFIG_YAMLFILE_CONTENT constant to 'mklists.yml'."""
    os.chdir(tmp_path)
    write_config_yamlfile()
    assert open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_CONTENT


def test_write_config_yamlfile_not_if_already_exists(tmp_path):
    os.chdir(tmp_path)
    Path(CONFIG_YAMLFILE_NAME).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_config_yamlfile()
