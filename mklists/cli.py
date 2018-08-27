"""CLI - command-line interface module"""

import glob
import yaml
import click
import os
import sys
from mklists import (
    MKLISTSRC, 
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER,
    LOCAL_RULEFILE_NAME, 
    LOCAL_RULEFILE_STARTER, 
    VALID_FILENAME_CHARS,
    ConfigFileNotFoundError,
    DatadirNotAccessibleError,
    AlreadyInitError
    )
from mklists.rules import parse_rules

@click.group()
@click.option('--datadir', type=str, metavar='DIRPATH',
              help="Use non-default data directory [./]")
@click.option('--globalrules', type=str, metavar='FILEPATH', 
              help="Set non-default global rules [./.globalrules]")
@click.option('--rules', type=str, metavar='FILEPATH', 
              help="Set non-default local rules [./.rules]")
@click.option('--backup', type=bool, is_flag=True,
              help="Back up input data [./.backups/]")
@click.option('--backup-dir', type=str, metavar='DIRPATH',
              help="Set non-default backup directory")
@click.option('--backup-depth', type=int, metavar='INTEGER',
              help="Set number of backups to keep [3]")
@click.option('--urlify', type=bool, is_flag=True,
              help="Copy data, urlified [./.html/]")
@click.option('--urlify-dir', type=str, metavar='DIRPATH',
              help="Set non-default urlified directory")
@click.option('--dryrun', type=bool, is_flag=True, 
              help="Run read-only and verbosely")
@click.option('--verbose', type=bool, is_flag=True, help="Run verbosely")
@click.version_option('0.1.3', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, globalrules, rules, 
        backup, backup_dir, backup_depth, 
        urlify, urlify_dir, 
        dryrun, verbose):
    """Tweak rules to rearrange plain-text todo lists"""

    if verbose:
        print('Running main command `mklists`.')

    ctx.obj = {
        'globalrules': None,
        'rules': '.rules',
        'datadir': '.',
        'urlify': False,
        'urlify_dir': '.urlified',
        'backup': False,
        'backup_dir': '.backups',
        'backup_depth': 3,
        'readonly': False,
        'verbose': False,
        'valid_filename_characters': VALID_FILENAME_CHARS,
        'invalid_filename_patterns': ['\.swp$', '\.tmp$', '~$', '^\.'],
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

    if globalrules:
        ctx.obj['globalrules'] = globalrules
        if verbose:
            print(f"Will use global rule file {repr(ctx.obj['global'])}.")

    if rules:
        ctx.obj['rules'] = rules
        if verbose:
            print(f"Will use local rule file {repr(ctx.obj['rules'])}.")

    if backup:
        ctx.obj['backup'] = backup
        if verbose:
            print(f"Will back up input data to {repr(ctx.obj['backup_dir'])}.")

    if urlify:
        ctx.obj['urlify'] = urlify
        if verbose:
            print(f"Will urlify data to {repr(ctx.obj['urlify_dir'])}.")

    if not os.path.exists(MKLISTSRC):
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")


@cli.command()
@click.pass_context
def init(ctx):
    """Generate initial configuration and rule files"""

    print(f"Global rules: {ctx.obj['globalrules']}")
    print(f"Local rules: {ctx.obj['rules']}")
    print(f"Default config: {MKLISTSRC}")
    sys.exit("Exiting")

    if not os.path.exists(MKLISTSRC):
        print(f"Creating default {repr(MKLISTSRC)} - customize as needed.")
        with open(MKLISTSRC, 'w') as fout:
            yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)
    else:
        raise AlreadyInitError(f"To re-initialize, first delete {MKLISTSRC}.")

    with open(MKLISTSRC) as configfile:
        ctx.obj.update(yaml.load(configfile))

    if verbose:
        print(f"Configuration - after reading {repr(MKLISTSRC)}:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)
        ctx.obj['verbose'] = verbose
        print(f"Checking for options set on command line...")

    if ctx.obj['globalrules']:
        if not os.path.exists(ctx.obj['globalrules']):
            print(f"Creating {repr(GLOBAL_RULEFILE_NAME)} - tweak as needed.")
            with open(GLOBAL_RULEFILE_NAME, 'w') as fout:
                fout.write(GLOBAL_RULE_FILE_STARTER)
        else:
            print(f"Found existing {repr(ctx.obj['globalrules'])}.")

    if not os.path.exists(ctx.obj['rules']):
        print(f"Creating {repr(LOCAL_RULEFILE_NAME)} - tweak as needed.")
        with open(LOCAL_RULEFILE_NAME, 'w') as fout:
            fout.write(LOCAL_RULE_FILE_STARTER)
    else:
        print(f"Found existing {repr(ctx.obj['rules'])}.")


@cli.command()
@click.pass_context
def run(ctx, urlify_dir, backup_dir, backup_depth):
    """Apply rules to re-write data"""

    if verbose:
        print('Running subcommand `run`.')
        print(f"Running in data directory {os.getcwd()}.")
        print(f"Using configuration:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    bad_patterns = ctx.obj['invalid_filename_patterns']
    global_rules = ctx.obj['globalrules']
    local_rules = ctx.obj['local_rules']
    rule_list = {}
    if global_rules:
        if verbose:
            print(f"Reading global rule file {repr(global_rules)}.")
        rule_list.extend(parse_rules(global_rules, bad_patterns))
    if verbose:
        print(f"Reading local rule file {repr(global_rules)}.")
    rule_list.extend(parse_rules(local_rules, bad_patterns))

    visible_files = [name for name in glob.glob('*')]
    print(f"* Something like: Datadir.get_datalines(datafiles=visible_files,")
    print(f"  not_matching=bad_patterns).")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")

    print(f"* Get datalines from files in {os.getcwd()}.")
    print(f"* Apply rules to datalines, modifying in-memory datadict.")
    print(f"* Backup option: Create time-stamped backup_dir.")
    print(f"* Backup option: Move existing files to backup_dir.")
    print(f"* Write out datadict values as files in datadir.")
    print(f"* HTML option: Write out datadict values as files in urlify_dir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")
