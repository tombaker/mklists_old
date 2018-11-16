"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILEA_STARTER_YAMLSTR,
    GLOBAL_RULEFILE_NAME,
    LOCAL_RULEFILE_NAME,
    VALID_FILENAME_CHARACTERS_STR,
)
from mklists.readwrite import write_initial_configfile, write_initial_rulefiles
from mklists.utils import write_yamlstr_to_yamlfile


@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Tests that two functions correctly round-trip:
    * write_initial_configfile()
    * _apply_overrides_from_file()"""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(configfile_name=mklistsrc)
    updated_context = _apply_overrides_from_file()
    assert (
        updated_context["valid_filename_characters"]
        == VALID_FILENAME_CHARACTERS_STR
    )


@pytest.mark.write
def test_write_initial_globalrules_isolated():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write_initial_rulefiles()
        assert (
            GLOBAL_RULEFILE_STARTER_YAMLSTR
            == open(GLOBAL_RULEFILE_NAME).read()
        )


@pytest.mark.write
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles()
    globalrules_name = tmpdir.join(".globalrules")
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(GLOBAL_RULEFILE_STARTER_YAMLSTR) == globalrules_hash


@pytest.mark.skip
def test_write_initial_localrules(tmpdir):
    """No longer taking local_rulefile_name as argument."""
    os.chdir(tmpdir)
    write_initial_rulefiles(local_rulefile_name=".localrules")
    localrules_name = tmpdir.join(".localrules")
    localrules_content = open(localrules_name).read()
    localrules_hash = hash(localrules_content)
    assert hash(LOCAL_RULEFILEA_STARTER_YAMLSTR) == localrules_hash
