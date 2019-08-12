"""@@@"""

import os
import pytest
import ruamel.yaml
from mklists.exceptions import ConfigFileNotFoundError
from mklists.run import return_configdict_from_config_yamlfile

config_yamlfile_name = "mklists.yml"

config_yamlfile_str = """verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}"""


def test_run_return_configdict_from_config_yamlfile(tmpdir):
    """ See /Users/tbaker/github/tombaker/mklists/mklists/run.py """
    os.chdir(tmpdir)
    expected = {
        "verbose": False,
        "html_yes": False,
        "backup_depth_int": 3,
        "invalid_filename_patterns": ["\\.swp$", "\\.tmp$", "~$", "^\\."],
        "files2dirs_dict": {},
    }
    tmpdir.join(config_yamlfile_name).write(config_yamlfile_str)
    assert (
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=config_yamlfile_name
        )
        == expected
    )


def test_run_return_configdict_from_config_yamlfile_notfound(tmpdir):
    """ See /Users/tbaker/github/tombaker/mklists/mklists/run.py """
    os.chdir(tmpdir)
    with pytest.raises(ConfigFileNotFoundError):
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=config_yamlfile_name
        )
