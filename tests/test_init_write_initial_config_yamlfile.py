"""
Here: /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile.py
"""

import io
import os
from mklists.initialize import (
    CONFIG_YAMLFILE_NAME,
    MINIMAL_CONFIG_YAMLFILE_STR,
    write_minimal_config_yamlfile,
)


def test_init_write_minimal_config_yamlfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_config_yamlfile()
    assert io.open(CONFIG_YAMLFILE_NAME).read() == MINIMAL_CONFIG_YAMLFILE_STR
