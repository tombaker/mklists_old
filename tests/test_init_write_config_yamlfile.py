"""
Here: /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile.py
"""

import io
import os
from mklists.constants import CONFIG_YAMLFILE_NAME, CONFIG_YAMLFILE_STR
from mklists.initialize import write_config_yamlfile


def test_init_write_config_yamlfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_config_yamlfile(
        _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
        _file_tobewritten_str=CONFIG_YAMLFILE_STR,
    )
    assert io.open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_STR
