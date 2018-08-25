"""CLI - command-line interface module

Issues: 
* chdir(datadir) right at beginning?
* flag to opt in/out of backup option? No - only question should be "where?"
* flag to opt in/out of HTML option?
"""

import yaml
import click
import os
from mklists import VALID_FILENAME_CHARS, MKLISTSRC, RULEFILE
from mklists.rules import parse_rules, DEFAULT_RULE_FILE

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
        print('Running main command `mklists`.')

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
        'bad_filename_patterns': ['\.swp$', '\.tmp$', '~$', '^\.'],
        'files2dirs': None}

    if datadir:
        try:
            os.chdir(datadir)
            if verbose:
                print(f"Setting current data directory: {repr(datadir)}.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{datadir} not accessible.")

    if verbose:
        print("Configuration - hardwired defaults:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    try:
        print(f"Configuration - try to read {repr(MKLISTSRC)}")
        with open(MKLISTSRC) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"{MKLISTSRC} not found.")

    if verbose:
        print(f"Configuration - after reading {repr(MKLISTSRC)}:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)
        ctx.obj['verbose'] = verbose  # set only after showing MKLISTSRC
        print(f"Configuration - checking for options set on command line")

    if rules:
        ctx.obj['rules'] = list(rules)
        if verbose:
            for rulefile in ctx.obj['rules']:
                print(f"Will use rule file {repr(rulefile)}.")

    if backup:
        ctx.obj['backup'] = backup
        if verbose:
            print(f"Will back up input data to {repr(ctx.obj['backup_dir'])}.")

    if urlify:
        ctx.obj['urlify'] = urlify
        if verbose:
            print(f"Will urlify data to {repr(ctx.obj['urlify_dir'])}.")


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize data folder"""

    if verbose:
        print('Running subcommand `init`.')

    all_rule_files = ctx.obj['rules'].extend(RULEFILE)
    for file in all_rule_files:
        if os.path.exists(file):
            sys.exit(f"To replace rule files, delete files and re-run.")
        else:
            if verbose:
                print(f"Creating default rule file - edit as desired.")
            with open(RULEFILE, 'w') as fout:
                fout.write(DEFAULT_RULE_FILE)

    if os.path.exists(MKLISTSRC):
        sys.exit(f"To replace {repr(MKLISTSRC)}, delete and re-run.")
    else:
        print(f"Creating default {repr(MKLISTSRC)} - edit as desired.")
        with open(MKLISTS, 'w') as fout:
            yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)


@cli.command()
@click.option('--urlify_dir', type=str, metavar='DIRPATH',
              help="Copy data files, urlified, to DIRPATH")
@click.option('--backup-dir', type=str, metavar='DIRPATH',
              help="Back up data files to DIRPATH")
@click.option('--backup-depth', type=int, metavar='INT',
              help="Backup depth [3]")
@click.pass_context
def make(ctx, urlify_dir, backup_dir, backup_depth):
    """Process lists as per rules"""

    if verbose:
        print('Running subcommand `make`.')

    session_datadir = ctx.obj['datadir']
    urlify_dir = ctx.obj['urlify_dir']
    backup_dir = ctx.obj['backup_dir']

    print(f"* Already got configuration in main mklists command.")
    print(f"* Already set datadir to {os.getcwd()}.")
    for rulefile in ctx.obj['rules']:
        print(f"* Get rules from file {repr(rulefile)}.")
    # rule_list = parse_rules(ctx.obj['rules'], ctx.obj['bad_filename_patterns'])
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

    if verbose:
        print('Running subcommand `verify`.')

    for rulefile in ctx.obj['rules']:
        print(f"* Get rules from file {repr(rulefile)}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


class ConfigError(SystemExit):
    """Category of errors related to configuration"""

class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file '.mklistsrc' was not found"""
    

class DatadirNotAccessibleError(ConfigError):
    """Non-default working data directory is not accessible"""
