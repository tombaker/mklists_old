"""@@@Docstring"""

import os
import yaml
from mklists.readwrite import read_settings_from_configfile

"""
    backup_dir = root_dir.mkdir(BACKUP_DIR_NAME)
    htmlfiles_dir = root_dir.mkdir(HTMLFILES_DIR_NAME)
    assert mklistsrc.read() == CONFIG_STARTER_DICT
"""


def test_read_settings_from_configfile(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {"backups": 6}
    with open(".config", "w") as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert read_settings_from_configfile(".config") == settings_dict
