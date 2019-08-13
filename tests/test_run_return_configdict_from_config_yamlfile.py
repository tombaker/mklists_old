"""@@@"""

import os
import pytest
from mklists.exceptions import ConfigFileNotFoundError, YamlFileNotFoundError
from mklists.run import return_configdict_from_config_yamlfile
from mklists.utils import return_yamlstr_from_yamlfile, return_pyobj_from_yamlstr

CONFIG_YAMLFILE_NAME = "mklists.yml"

CONFIG_YAMLFILE_STR = r"""verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}"""

CONFIG_YAMLFILE_STR_COMMENTED_OUT = r"""verbose: false
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
    tmpdir.join(CONFIG_YAMLFILE_NAME).write(CONFIG_YAMLFILE_STR)
    assert (
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=CONFIG_YAMLFILE_NAME
        )
        == expected
    )


def test_run_yamlstr_written_correctly_to_file(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    tmpdir.join(CONFIG_YAMLFILE_NAME).write(CONFIG_YAMLFILE_STR_COMMENTED_OUT)
    assert CONFIG_YAMLFILE_STR_COMMENTED_OUT == open(CONFIG_YAMLFILE_NAME).read()


def test_run_return_configdict_from_config_yamlfile_with_entries_commented_out(tmpdir):
    """In this example, many of the entries are commented out."""
    os.chdir(tmpdir)
    expected = {"verbose": False}
    tmpdir.join(CONFIG_YAMLFILE_NAME).write(CONFIG_YAMLFILE_STR_COMMENTED_OUT)
    assert (
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=CONFIG_YAMLFILE_NAME
        )
        == expected
    )


@pytest.mark.skip
def test_run_return_configdict_from_config_yamlfile_notfound(tmpdir):
    """ See /Users/tbaker/github/tombaker/mklists/mklists/run.py """
    os.chdir(tmpdir)
    with pytest.raises(ConfigFileNotFoundError):
        return_configdict_from_config_yamlfile(
            _config_yamlfile_name=CONFIG_YAMLFILE_NAME
        )
