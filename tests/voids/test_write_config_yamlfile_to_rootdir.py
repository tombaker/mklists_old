"""Writes YAML configuration file, 'mklists.yml', to repo root directory."""

import os
import pytest
from pathlib import Path
from mklists.constants import CONFIGFILE_CONTENT, CONFIGFILE_NAME
from mklists.voids import write_config_yamlfile


def test_write_config_yamlfile(tmp_path):
    """Write contents of CONFIGFILE_CONTENT constant to 'mklists.yml'."""
    os.chdir(tmp_path)
    write_config_yamlfile()
    assert open(CONFIGFILE_NAME).read() == CONFIGFILE_CONTENT


def test_write_config_yamlfile_not_if_already_exists(tmp_path):
    os.chdir(tmp_path)
    Path(CONFIGFILE_NAME).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_config_yamlfile()
