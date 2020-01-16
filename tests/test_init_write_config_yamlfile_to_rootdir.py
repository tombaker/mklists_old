"""Tests write_config_yamlfile_to_rootdir"""

import io
import os
import pytest
import ruamel.yaml
import attr
from mklists.constants import Settings
from mklists.initialize import write_config_yamlfile_from_settingsobj_to_rootdir
from mklists.run import read_config_yamlfile_return_config_dict


@pytest.mark.skip
def test_init_write_config_yamlfile_from_settingsobj_to_rootdir(tmpdir):
    """Write contents of Settings() instance to YAML config file 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile_from_settingsobj_to_rootdir()
    assert read_config_yamlfile_return_config_dict() == attr.asdict(Settings())
