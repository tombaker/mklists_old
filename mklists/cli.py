"""CLI - command-line interface module"""

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
    VALID_FILENAME_CHARS)
from mklists.rules import parse_rules

@click.group()
@click.option('--datadir', type=str, metavar='DIRPATH',
              help="Set DIRPATH as current data directory")
@click.option('--globalrules', type=str, metavar='FILENAME', 
              help="Use optional global rules, read before local rules")
@click.option('--rules', type=str, metavar='FILENAME', 
              help="Use local rules other than default '.rules'")
@click.option('--init', type=bool, is_flag=True,
              help="Write config files for first-time dryrun")
@click.option('--backup', type=bool, is_flag=True,
              help="Back up input data to '.backups/YYYYMMDD_HHMMSS/'")
@click.option('--urlify', type=bool, is_flag=True,
              help="Copy output data, urlified, to '.urlified/'")
@click.option('--verbose', type=bool, is_flag=True, help="Run verbosely")
@click.version_option('0.1.3', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, globalrules, rules, init, backup, urlify, verbose):
    """Evolve plain-text todo lists by tweaking rules"""

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

    if not os.path.exists(MKLISTSRC):
        print(f"Required configuration file {repr(MKLISTSRC)} not found.")
        if init:
            print(f"Creating default {repr(MKLISTSRC)} - customize as needed.")
            with open(MKLISTSRC, 'w') as fout:
                yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)
        else:
            raise ConfigFileNotFoundError(f"Run `mklists --init dryrun`.")
    
    with open(MKLISTSRC) as configfile:
        ctx.obj.update(yaml.load(configfile))
        if verbose:
            print(f"Configuration - after reading {repr(MKLISTSRC)}")

    if verbose:
        print(f"Configuration - after reading {repr(MKLISTSRC)}:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)
        ctx.obj['verbose'] = verbose
        print(f"Checking for options set on command line...")

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

    if verbose:
        print(f"Configuration - after overriding with command-line options:"
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    if not os.path.exists(ctx.obj['globalrules']):
        if init:
            print(f"Creating {repr(GLOBAL_RULEFILE_NAME)} - tweak as needed.")
            with open(GLOBAL_RULEFILE_NAME, 'w') as fout:
                fout.write(GLOBAL_RULE_FILE_STARTER)

    if not os.path.exists(ctx.obj['rules']):
        if init:
            print(f"Creating {repr(LOCAL_RULEFILE_NAME)} - tweak as needed.")
            with open(LOCAL_RULEFILE_NAME, 'w') as fout:
                fout.write(LOCAL_RULE_FILE_STARTER)

    if not os.path.exists(ctx.obj['rules']):
    for rulefile in global_rules local_rules:
        exists = os.path.exists(rulefile)
        if exists:
            at_least_one_rulefile_exists = True
        else:
            print(f"Warning: {rulefile} does not exist or not accessible.")

        local_rules = ctx.obj['rules']


@cli.command()
@click.pass_context
def dryrun(ctx):
    """Read-only dry run (see also --init)"""

    if verbose:
        print('Running subcommand `dryrun`.')

    for rulefile in ctx.obj['rules']:
        print(f"* Get rules from file {repr(rulefile)}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


@cli.command()
@click.option('--urlify-dir', type=str, metavar='DIRPATH',
              help="Copy data files, urlified, to DIRPATH")
@click.option('--backup-dir', type=str, metavar='DIRPATH',
              help="Back up data files to DIRPATH")
@click.option('--backup-depth', type=int, metavar='INT',
              help="Backup depth [3]")
@click.pass_context
def run(ctx, urlify_dir, backup_dir, backup_depth):
    """Process and rewrite lists as per rules"""

    if verbose:
        print('Running subcommand `run`.')

    if init:
        print(f"Warning: consider tweaking default {ctx.obj['rules']} first.")
        if input(f"Proceed anyway?\nENTER to continue or any key to exit."):
            sys.exit()

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



class ConfigError(SystemExit):
    """Category of errors related to configuration"""


class ConfigFileNotFoundError(ConfigError):
    """Hardwired configuration file '.mklistsrc' was not found"""
    

class DatadirNotAccessibleError(ConfigError):
    """Non-default working data directory is not accessible"""
