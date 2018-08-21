"""CLI - command-line interface module

Issue: where to do chdir(datadir)?  
"""

import yaml
import click
from mklists import VALID_FILENAME_CHARS


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

    ### CHANGE HERE TO WORKING DIRECTORY

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
        'valid_filename_characters': None,
        'files2dirs': None,
        'bad_filename_patterns': ['\.swp$', '\.tmp$', '~$', '^\.']}

    # maybe -vv with count=True?
    if debug:
        click.echo('Hardwired configuration defaults:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # Try to read configfile and use it to update ctx.obj
    try:
        with open('.mklistsrc') as configfile:
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

    print(f"Create editable rule file: '.rules' with defaults.")
    print(f"If rule file already exists, print warning and skip.")
    print(f"Create mandatory config file '.mklistsrc'.")
    print(f"If config file already exists, print warning and skip.")
    # yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)


@cli.command()
@click.pass_context
def make(ctx):
    """Remake lists as per rules"""

    print(f"* Try to get rules: {repr(ctx.obj['rules'])}.")
    print(f"* Get data: {repr(ctx.obj['datadir'])}.")
    print(f"* Apply rules to data, modifying data dictionary.")
    print(f"* Create (or use) time-stamped folder within backup folder.")
    print(f"* Move files to time-stamped backup folder.")
    print(f"* Write out data dictionary as files in data folder.")
    print(f"* Move files as per ['files2dirs'].")


@cli.command()
@click.pass_context
def verify(ctx):
    """Check rules and data folder, verbosely"""

    print(f"* Get rules: {repr(ctx.obj['rules'])}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


class ConfigFileNotFoundError(SystemExit):
    """Specified (non-default) configuration file was not found"""
