"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import VALID_FILENAME_CHARACTERS_STR
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
