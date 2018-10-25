"""@@@Docstring"""

import pytest
import click
import os
from click.testing import CliRunner
from mklists.cli import cli
from mklists import (MKLISTSRC, STARTER_DEFAULTS, STARTER_GLOBALRULES, 
    STARTER_LOCALRULES, STARTER_GRULEFILE_NAME, STARTER_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from pathlib import Path



@pytest.mark.skip
def test_cli():
    runner = CliRunner()
    new_rulefile_name = '.local_rules'
    with runner.isolated_filesystem():
        Path(MKLISTSRC).touch()
        Path(new_rulefile_name).touch()
        result = runner.invoke( cli, 
                    ['--verbose', 
                     '--dryrun', 
                     '--rules', 
                     new_rulefile_name, 
                     'run'])
    assert '.local_rules' in result.output

