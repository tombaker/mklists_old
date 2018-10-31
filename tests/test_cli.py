"""@@@Docstring"""

import pytest
import click
import os
from click.testing import CliRunner
from mklists.cli import cli
from mklists.cli.cli import apply_overrides_from_cli
#from mklists.readwrite import (
#    get_settings_from_cli, 
#    apply_overrides_from_cli)
from mklists import (MKLISTSRC_NAME, BUILTIN_MKLISTSRC, BUILTIN_GRULES, 
    BUILTIN_LRULES, BUILTIN_GRULEFILE_NAME, BUILTIN_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from pathlib import Path


@pytest.mark.cli
def test_cli_set_datadir(cwd_configured):
    """@@@docstring"""
    runner = CliRunner()
    runner.invoke(cli, args=[
        '--datadir', 
        '/Users/tbaker/mydata', 
        'run'])
    print(cli.apply_overrides_from_cli())
    #print(get_settings_from_cli(cli_settings=locals())['datadir'])
    #print(apply_overrides_from_cli())
    #assert get_settings_from_cli()['datadir'] == apply_overrides_from_cli()['datadir']
    #assert get_settings_from_cli() == 'what'
    #assert 0

#   --datadir DIRPATH       Set working directory [default './']
#   --globalrules FILEPATH  Set global rules [default './.globalrules']
#   --rules FILEPATH        Set local rules [default './.rules']
#   --backup                Enable backups
#   --backup-dir DIRPATH    Set backups directory [default './.backups/']
#   --backup-depth INTEGER  Set backups to keep [default: '3']
#   --urlify                Enable generation of HTML output
#   --urlify-dir DIRPATH    Set HTML directory [default: './.html/']
#   --dryrun                Run in read-only mode, for debugging
#   --verbose               Enable verbose mode
#   --version               Show version and exit
#   --help                  Show help and exit
# 
# Commands:
#   init  Generate default configuration and rule...
#   run   Apply rules to re-write data files
