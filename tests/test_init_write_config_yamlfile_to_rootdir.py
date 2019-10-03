"""
Here: /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile.py
"""

import io
import os
import pytest

# from mklists.constants import CONFIG_YAMLFILE_NAME, CONFIG_YAMLFILE_STR
from mklists.initialize import write_config_yamlfile_to_rootdir


@pytest.mark.skip
def test_init_write_config_yamlfile_to_rootdir(tmpdir):
    """2019-10-03: Will no longer get configuration from file, but Python dataclass.
    * Write initial YAML config file 'mklists.yml'."""
    os.chdir(tmpdir)
    write_config_yamlfile_to_rootdir(
        file_tobewritten_name=None, file_tobewritten_str=None
    )
    # assert io.open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_STR
