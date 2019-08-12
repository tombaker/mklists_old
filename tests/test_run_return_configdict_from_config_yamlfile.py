"""@@@"""

import os
import pytest
from mklists.exceptions import ConfigFileNotFoundError
from mklists.run import return_configdict_from_config_yamlfile
from mklists.utils import return_pyobj_from_yamlfile

config_yamlfile_name = "mklists.yml"

config_yamlfile_str = r"""verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}"""

config_yamlfile_str_commented_out = r"""verbose: false
# html_yes: false
"""


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


def test_run_yamlstr_written_correctly_to_file(tmpdir):
    os.chdir(tmpdir)
    tmpdir.join(config_yamlfile_name).write(config_yamlfile_str_commented_out)
    assert config_yamlfile_str_commented_out == open(config_yamlfile_name).read()


def test_run_return_configdict_from_config_yamlfile_with_entries_commented_out(tmpdir):
    """In this example, many of the entries are commented out."""
    os.chdir(tmpdir)
    expected = {"verbose": False}
    tmpdir.join(config_yamlfile_name).write(config_yamlfile_str_commented_out)
    assert (
        return_pyobj_from_yamlfile(_generic_yamlfile_name=config_yamlfile_name)
        == expected
    )
    assert (
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=config_yamlfile_name
        )
        == expected
    )
