"""@@@Docstring"""


import os
import pytest
from mklists.config import (
    CONFIG_YAMLFILE_NAME,
    RULES_CSVFILE_NAME,
    BACKUPDIR_NAME,
    HTMLDIR_NAME,
)


def test_defaults_config_yamlfile_name():
    assert CONFIG_YAMLFILE_NAME == "mklists.yml"
    assert RULES_CSVFILE_NAME == ".rules"
    assert BACKUPDIR_NAME == "backups"
    assert HTMLDIR_NAME == "html"


def test_defaults_cwd(tmpdir):
    STARTDIR_PATHNAME = tmpdir
    os.chdir(tmpdir)
    assert STARTDIR_PATHNAME == tmpdir
