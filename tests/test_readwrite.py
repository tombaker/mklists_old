"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (
    MKLISTSRC_LOCAL_NAME,
    MKLISTSRC_STARTER_DICT,
    GLOBAL_RULEFILE_STARTER_YAMLSTRING,
    LOCAL_RULEFILE_STARTER_YAMLSTRING,
    GLOBAL_RULEFILE_NAME,
    LOCAL_RULEFILE_NAME,
    VALID_FILENAME_CHARS,
)
from mklists.readwrite import (
    write_initial_rulefiles,
    write_initial_configfile,
    write_yamlstr_to_yamlfile,
)


@pytest.mark.write
def test_write_initial_globalrules_isolated():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write_initial_rulefiles(
            global_rulefile_name=GLOBAL_RULEFILE_NAME,
            globalrules_content=GLOBAL_RULEFILE_STARTER_YAMLSTRING,
        )
        assert (
            GLOBAL_RULEFILE_STARTER_YAMLSTRING
            == open(GLOBAL_RULEFILE_NAME).read()
        )


@pytest.mark.write
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(global_rulefile_name=".globalrules")
    globalrules_name = tmpdir.join(".globalrules")
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(GLOBAL_RULEFILE_STARTER_YAMLSTRING) == globalrules_hash


@pytest.mark.write
def test_write_initial_localrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(local_rulefile_name=".localrules")
    localrules_name = tmpdir.join(".localrules")
    localrules_content = open(localrules_name).read()
    localrules_hash = hash(localrules_content)
    assert hash(LOCAL_RULEFILE_STARTER_YAMLSTRING) == localrules_hash
