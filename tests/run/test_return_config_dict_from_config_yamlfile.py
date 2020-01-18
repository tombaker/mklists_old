"""@@@"""

import os
import pytest
from mklists.constants import CONFIG_YAMLFILE_NAME
from mklists.exceptions import ConfigFileNotFoundError
from mklists.run import return_config_dict_from_config_yamlfile
from mklists.utils import return_rootdir_pathname

CONFIG_YAMLFILE_CONTENT = (
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


def test_return_config_dict_from_config_yamlfile(tmpdir):
    """ See /Users/tbaker/github/tombaker/mklists/mklists/run.py """
    os.chdir(tmpdir)
    here = return_rootdir_pathname(startdir_pathname=os.getcwd())
    tmpdir.join(CONFIG_YAMLFILE_NAME).write(CONFIG_YAMLFILE_CONTENT)
    assert (
        return_config_dict_from_config_yamlfile(rootdir_pathname=here) == CONFIG_PYOBJ
    )


def test_run_read_config_yamlfile_return_config_dict_with_entries_commented_out(tmpdir):
    """In this example, many of the entries are commented out."""
    os.chdir(tmpdir)
    CONTENT = "verbose: False\n" "# htmlify: True\n"
    expected = {"verbose": False}
    tmpdir.join(CONFIG_YAMLFILE_NAME).write(CONTENT)
    assert return_config_dict_from_config_yamlfile() == expected


def test_run_read_config_yamlfile_return_config_dict_not_found(tmpdir):
    """ See /Users/tbaker/github/tombaker/mklists/mklists/run.py """
    os.chdir(tmpdir)
    here = return_rootdir_pathname(startdir_pathname=os.getcwd())
    with pytest.raises(SystemExit):
        return_config_dict_from_config_yamlfile(rootdir_pathname=here)
