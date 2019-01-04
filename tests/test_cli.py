"""@@@Docstring"""

import os
import yaml
from mklists.readwrite import read_settings_from_configfile


def test_read_settings_from_configfile(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {"backups": 6}
    with open(".config", "w") as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert read_settings_from_configfile(".config") == settings_dict
