"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    GLOBAL_RULEFILE_NAME,
    VALID_FILENAME_CHARACTERS_STR,
)
from mklists.cli import _write_initial_configfile, _write_initial_rulefiles
from mklists.utils import write_yamlstr_to_yamlfile


@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Write mklists.yml, then read it back."""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(MKLISTS_YML_NAME)
    _write_initial_configfile(configfile_name=mklistsrc)
    updated_context = _apply_overrides_from_file()
    assert (
        updated_context["valid_filename_characters"]
        == VALID_FILENAME_CHARACTERS_STR
    )


@pytest.mark.skip
def test_write_initial_globalrules_isolated():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _write_initial_rulefiles()
        assert (
            GLOBAL_RULEFILE_STARTER_YAMLSTR
            == open(GLOBAL_RULEFILE_NAME).read()
        )


@pytest.mark.skip
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    _write_initial_rulefiles()
    globalrules_name = tmpdir.join(".globalrules")
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(GLOBAL_RULEFILE_STARTER_YAMLSTR) == globalrules_hash
