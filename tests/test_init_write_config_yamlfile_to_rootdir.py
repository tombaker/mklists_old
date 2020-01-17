"""Writes YAML configuration file, 'mklists.yml', to repo root directory."""

import io
import os
import pytest
from mklists.constants import (
    CONFIG_YAMLFILE_CONTENT,
    CONFIG_YAMLFILE_NAME,
    RULES_CSVFILE_NAME,
)
from mklists.initialize import write_config_yamlfile_to_rootdir


def test_init_write_config_yamlfile_to_rootdir(tmpdir):
    """Write contents of CONFIG_YAMLFILE_CONTENT constant to 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile_to_rootdir()
    print(os.getcwd())
    print(os.path.join(os.getcwd(), CONFIG_YAMLFILE_NAME))
    print(os.listdir(os.getcwd()))
    print(os.path.getsize(os.path.join(os.getcwd(), CONFIG_YAMLFILE_NAME)))
    print(str(tmpdir))
    assert open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_CONTENT
