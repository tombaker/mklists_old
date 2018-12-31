"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists.goto import set_rootdir
from mklists import CONFIGFILE_NAME


@pytest.mark.finddirs
def test_set_rootdir(tmpdir):
    """Find and set root directory."""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(CONFIGFILE_NAME)
    # _write_initial_configfile(configfile_name=mklistsrc)
    # updated_context = _apply_overrides_from_file()
    assert False
