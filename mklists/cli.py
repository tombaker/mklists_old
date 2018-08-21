"""CLI - command-line interface module

Issues: 
* chdir(datadir) right at beginning?
* flag to opt in/out of backup option? No - only question should be "where?"
* flag to opt in/out of HTML option?
"""

import yaml
import click
import os
from mklists import VALID_FILENAME_CHARS, MKLISTSRC


@click.group()
@click.option('--datadir', type=str, metavar='DIRPATH',
              help="Working data directory [.]")
@click.option('--rules', type=str, metavar='FILENAME', multiple=True,
              help="Rule file - repeatable [.rules]")
@click.option('--htmldir', type=str, metavar='DIRPATH',
              help="Urlified-data directory [.html]")
@click.option('--backupdir', type=str, metavar='DIRPATH',
              help="Backup folder [.backups]")
@click.option('--backup-depth', type=int, metavar='INT',
              help="Backup depth [3]")
@click.option('--debug', type=bool, is_flag=True,
              help="Run verbosely")
@click.version_option('0.1.3', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, rules, htmldir, backupdir, backup_depth, debug):
    """Tweak plain-text todo lists by rules"""

    ### CHANGE HERE TO WORKING DIRECTORY - test:

    if debug:
        print('Printing diagnostic information.')
        print(VALID_FILENAME_CHARS)

    # Hardwired default values (before reading '.mklistsrc')
    ctx.obj = {
        'rules': ['.rules', ],
        'datadir': '.',
        'htmldir': '.html',
        'backupdir': '.backups',
        'backup_depth': 3,
        'debug': False,
        'verbose': False,
        'valid_filename_characters': VALID_FILENAME_CHARS,
        'files2dirs': None,
        'bad_filename_patterns': ['\.swp$', '\.tmp$', '~$', '^\.']}

    # maybe -vv with count=True?
    if debug:
        click.echo('Hardwired configuration defaults:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # Try to read configfile and use it to update ctx.obj
    try:
        with open(MKLISTSRC) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"Mandatory {repr(config)} not found.")

    if debug:
        print('Config settings after reading config file:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # if 'rules' set on command line, possibly repeated
    if rules:
        ctx.obj['rules'] = list(rules)
        if debug:
            # for rulefile in rules:
            print(f"Using rule file(s) {repr(ctx.obj['rules'])}.")

    if datadir:
        ctx.obj['datadir'] = datadir
        if debug:
            print(f"Using data folder {repr(ctx.obj['datadir'])}.")

    if htmldir:
        ctx.obj['htmldir'] = htmldir
        if debug:
            print(f"Using urlified data folder {repr(ctx.obj['htmldir'])}.")

    if backupdir:
        ctx.obj['backupdir'] = backupdir
        if debug:
            print(f"Using backups folder {repr(ctx.obj['backupdir'])}.")

    if backup_depth:
        ctx.obj['backup_depth'] = backup_depth
        if debug:
            print(f"Will keep last {str(backup_depth)} backups.")

    if debug:
        ctx.obj['debug'] = debug
        print('Final config settings:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize data folder"""

    print(f"Create basic '.rules' - or if exists, print warning and skip.")
    print(f"Create '.mklistsrc' - or if exists, print warning and skip.")
    # yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)


@cli.command()
@click.pass_context
def make(ctx):
    """Remake lists as per rules"""

    print(f"* Already got configuration in main mklists command.")
    print(f"* Already set datadir to current working directory.")
    print(f"* Initialize datadict from with datalines from files in datadir.")
    print(f"* Get rules from rulefiles (in principle anywhere).")
    print(f"* Apply rules to datalines, modifying in-memory datadict.")
    print(f"* Backup option: Create time-stamped backupdir.")
    print(f"* Backup option: Move existing files to backupdir.")
    print(f"* Write out datadict values as files in datadir.")
    print(f"* HTML option: Write out datadict values as files in htmldir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")


@cli.command()
@click.pass_context
def verify(ctx):
    """Check rules and data folder, verbosely"""

    rules = ctx.obj['rules']

    for rulefile in rules:
        print(f"* Get rules from file {repr(rulefile)}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


class ConfigFileNotFoundError(SystemExit):
    """Specified (non-default) configuration file was not found"""
