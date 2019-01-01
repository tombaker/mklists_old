"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists.utils import get_rootdir
from mklists import CONFIGFILE_NAME


@pytest.mark.skip
def test_get_rootdir(tmpdir):
    """Find and set root directory."""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(CONFIGFILE_NAME)
    # _write_initial_configfile(configfile_name=mklistsrc)
    # updated_context = _apply_overrides_from_file()
    assert False


# /tmp/root/mklists.yml
# /tmp/root/a/.rules
# /tmp/root/a/b/.rules
# /tmp/rootx/a/.rules
# /tmp/rootx/a/b/stackover.txt
# /tmp/rootx/a/b/.localrules
# /tmp/rooty/mklists.yml
# /tmp/rooty/a/.rules
# /tmp/rooty/a/b/.localrules
