"""@@@"""

import io
import os
from mklists.initialize import (
    CONFIG_YAMLFILE_NAME,
    INITIAL_CONFIG_YAMLFILE_STR,
    write_initial_config_yamlfile,
)


def test_initialize_write_initial_config_yamlfile(tmpdir):
    os.chdir(tmpdir)
    write_initial_config_yamlfile()
    configfile = os.path.join(tmpdir, CONFIG_YAMLFILE_NAME)
    assert io.open(configfile).read() == INITIAL_CONFIG_YAMLFILE_STR
