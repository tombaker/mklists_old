"""Tests write_config_yamlfile_to_rootdir"""

import io
import os
import pytest
import ruamel.yaml
from mklists.config import Defaults, Settings
from mklists.initialize import write_config_yamlfile_from_default_pyobj_to_rootdir

set = Settings()


@pytest.mark.skip
def test_init_write_config_yamlfile_from_default_pyobj_to_rootdir(tmpdir):
    """Write contents of Settings() instance to YAML config file 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile_from_default_pyobj_to_rootdir(
        rootdir_pathname=tmpdir,
        config_yamlfile_name=Defaults.config_yamlfile_name,
        pyobj=set,
    )
    expected = ""
    assert io.open(Defaults.config_yamlfile_name).read() == expected
