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
              help="Set DIRPATH as current data directory")
@click.option('--rules', type=str, metavar='FILENAME', multiple=True,
              help="Use non-default rule file - repeatable")
@click.option('--backup', type=bool, is_flag=True,
              help="Back up input data to .backups/YYYYMMDD_HHMMSS/")
@click.option('--urlify', type=bool, is_flag=True,
              help="Copy output data, urlified, to .urlified/")
@click.option('--verbose', type=bool, is_flag=True, help="Run verbosely")
@click.version_option('0.1.3', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, rules, backup, urlify, verbose):
    """Evolve plain-text todo lists by tweaking rules"""

    if verbose:
        print('Running in verbose mode.')

    # Hardwired default values (before reading '.mklistsrc')
    ctx.obj = {
        'rules': ['.rules', ],
        'datadir': '.',
        'urlify': False,
        'urlify_dir': '.urlified',
        'backup': False,
        'backup_dir': '.backups',
        'backup_depth': 3,
        'verbose': False,
        'verbose': False,
        'valid_filename_characters': VALID_FILENAME_CHARS,
        'files2dirs': None,
        'bad_filename_patterns': ['\.swp$', '\.tmp$', '~$', '^\.']}

    if datadir:
        session_datadir = datadir
        try:
            os.chdir(session_datadir)
            if verbose:
                print(f"Changing to working directory {repr(session_datadir)}.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{datadir} not accessible.")

    if verbose:
        click.echo('Hardwired configuration defaults:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # Try to read configfile and use it to update ctx.obj
    try:
        with open(MKLISTSRC) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"{repr(MKLISTSRC)} not found.")

    if verbose:
        print('Config settings after reading config file:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # if 'rules' set on command line, possibly repeated
    if rules:
        ctx.obj['rules'] = list(rules)
        if verbose:
            for rulefile in rules:
                print(f"Will use rule file {repr(rulefile)}.")

    if urlify:
        ctx.obj['urlify'] = urlify
        urlify_dir = ctx.obj['urlify_dir']
        if verbose:
            print(f"Will mirror output data, urlified, to {repr(urlify_dir)}.")

    if backup:
        ctx.obj['backup'] = backup
        backup_dir = ctx.obj['backup_dir']
        if verbose:
            print(f"Will back up input data to {repr(backup_dir)}.")

    if verbose:
        ctx.obj['verbose'] = verbose
        print('Final config settings:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize data folder (or reset to defaults)"""

    print(f"Create basic '.rules' or, if already exists, ask to replace.")
    print(f"Create '.mklistsrc' or, if already exists, ask to replace.")
    # if MKLISTS exists:
    #    prompt: replace?
    # with open(MKLISTS), 'w') as fout:
    #     yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)


@cli.command()
@click.option('--urlify_dir', type=str, metavar='DIRPATH',
              help="Copy data files, urlified, to DIRPATH")
@click.option('--backup-dir', type=str, metavar='DIRPATH',
              help="Back up data files to DIRPATH")
@click.pass_context
def make(ctx, urlify_dir, backup_dir):
    """Process lists as per rules"""

    session_datadir = ctx.obj['datadir']
    urlify_dir = ctx.obj['urlify_dir']
    backup_dir = ctx.obj['backup_dir']

    print(f"* Already got configuration in main mklists command.")
    print(f"* Already set datadir to {os.getcwd()}.")
    for rulefile in ctx.obj['rules']:
        print(f"* Get rules from file {repr(rulefile)}.")
    print(f"* Get datalines from files in {repr(session_datadir)}.")
    print(f"* Apply rules to datalines, modifying in-memory datadict.")
    print(f"* Backup option: Create time-stamped backup_dir.")
    print(f"* Backup option: Move existing files to backup_dir.")
    print(f"* Write out datadict values as files in datadir.")
    print(f"* HTML option: Write out datadict values as files in urlify_dir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")


@cli.command()
@click.pass_context
def verify(ctx):
    """Check rules and data folder, verbosely"""

    for rulefile in ctx.obj['rules']:
        print(f"* Get rules from file {repr(rulefile)}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


class ConfigError(SystemExit):
    """Category of errors related to configuration"""

class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file '.mklistsrc' was not found"""
    

class DatadirNotAccessibleError(ConfigError):
    """Non-default working data directory is not accessible"""
