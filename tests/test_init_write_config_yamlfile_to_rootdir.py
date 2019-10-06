"""Tests write_config_yamlfile_to_rootdir"""

import io
import os
import pytest
import ruamel.yaml
import attr
from mklists.config import Settings
from mklists.initialize import write_config_yamlfile_from_settingsobj_to_rootdir
from mklists.utils import return_config_dict_from_config_yamlfile


def test_init_write_config_yamlfile_from_settingsobj_to_rootdir(tmpdir):
    """Write contents of Settings() instance to YAML config file 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile_from_settingsobj_to_rootdir(str(tmpdir))
    assert return_config_dict_from_config_yamlfile() == attr.asdict(Settings())
