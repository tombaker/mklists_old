"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from mklists.constants import CONFIGFILE_NAME
from mklists.reads import read_configfile

CONFIGFILE_CONTENT = (
    "verbose: True\n"
    "htmlify: True\n"
    "backup_depth: 3\n"
    "invalid_filename_patterns:\n"
    "- \.swp$\n"
    "- \.tmp$\n"
    "- ~$\n"
    "- ^\.\n"
    "\n"
    "# For given file, destination directory to which it should be moved\n"
    "files2dirs:\n"
    "    to_a.txt: a\n"
    "    to_b.txt: b\n"
    "    to_c.txt: /Users/foo/logs\n"
)

CONFIG_PYOBJ = {
    "verbose": True,
    "htmlify": True,
    "backup_depth": 3,
    "invalid_filename_patterns": ["\\.swp$", "\\.tmp$", "~$", "^\\."],
    "files2dirs": {"to_a.txt": "a", "to_b.txt": "b", "to_c.txt": "/Users/foo/logs"},
}


def test_read_configfile(tmp_path):
    """Return dictionary of configuration settings from YAML file."""
    os.chdir(tmp_path)
    Path(CONFIGFILE_NAME).write_text(CONFIGFILE_CONTENT)
    assert read_configfile() == CONFIG_PYOBJ


def test_read_configfile_read_configfile_with_entries_commented_out(tmp_path):
    """Return configuration dictionary even if some lines are commented out."""
    os.chdir(tmp_path)
    configfile_content = "verbose: False\n" "# htmlify: True\n"
    Path(CONFIGFILE_NAME).write_text(configfile_content)
    expected = {"verbose": False}
    assert read_configfile() == expected


def test_systemexit_if_configfile_not_found(tmp_path):
    """Raise exception if no configuration YAML file is found."""
    os.chdir(tmp_path)
    with pytest.raises(SystemExit):
        read_configfile()


def test_systemexit_if_configfile_not_found_explicitly_specifying_rootdir(tmp_path):
    """Raise exception if no config file found when explicitly specifying rootdir."""
    os.chdir(tmp_path)
    cwd = Path.cwd()
    with pytest.raises(SystemExit):
        read_configfile(rootdir_pathname=cwd)


def test_systemexit_if_configfile_has_bad_yaml(tmp_path):
    """Raise exception if config file has bad YAML."""
    os.chdir(tmp_path)
    configfile_content = "BAD: -: @@YAML CONTENT@@\n"
    Path(CONFIGFILE_NAME).write_text(configfile_content)
    with pytest.raises(SystemExit):
        read_configfile()
