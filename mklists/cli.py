"""CLI - command-line interface module"""

import glob
import yaml
import click
import os
import sys
from mklists import (
    MKLISTSRC,
    STARTER_GLOBAL_RULEFILE,
    STARTER_LOCAL_RULEFILE,
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
@click.option('--readonly', type=bool, is_flag=True, help="Run read-only")
@click.option('--verbose', type=bool, is_flag=True, help="Run verbosely")
@click.version_option('0.1.3', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, globalrules, rules,
        backup, backup_dir, backup_depth,
        urlify, urlify_dir,
        readonly, verbose):
    """Tweak rules to rearrange plain-text todo lists"""

    if not os.path.exists(MKLISTSRC):
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

    ctx.obj = {
        'globalrules': '.globalrules',
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
                print(f"Setting {repr(datadir)} as current data directory.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{datadir} not accessible.")

    def assign_to_ctxobj(context, ctxobj_key, value):
        if value:
            context.obj[ctxobj_key] = value

    assign_to_ctxobj(ctx, 'globalrules', globalrules)
    assign_to_ctxobj(ctx, 'rules', rules)
    assign_to_ctxobj(ctx, 'urlify', urlify)
    assign_to_ctxobj(ctx, 'urlify_dir', urlify_dir)
    assign_to_ctxobj(ctx, 'backup', backup)
    assign_to_ctxobj(ctx, 'backup_dir', backup_dir)
    assign_to_ctxobj(ctx, 'backup_depth', backup_depth)
    assign_to_ctxobj(ctx, 'readonly', readonly)
    assign_to_ctxobj(ctx, 'verbose', verbose)

    if verbose:
        print("Using configuration:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)


@cli.command()
@click.pass_context
def init(ctx):
    """Generate default configuration and rule files"""

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

    if ctx.obj['verbose']:
        print(f"Configuration - after reading {repr(MKLISTSRC)}:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)
        print(f"Checking for options set on command line...")

    # Rules
    global_rules = ctx.obj['globalrules']
    if global_rules:
        if not os.path.exists(global_rules):
            print(f"Creating {global_rules} - tweak as needed.")
            with open(global_rules, 'w') as fout:
                fout.write(STARTER_GLOBAL_RULEFILE)
        else:
            print(f"Found existing {repr(global_rules)}.")

    local_rules = ctx.obj['rules']
    if not os.path.exists(local_rules):
        print(f"Creating {repr(local_rules)} - tweak as needed.")
        with open(local_rules, 'w') as fout:
            fout.write(STARTER_LOCAL_RULEFILE)
    else:
        print(f"Found existing {repr(ctx.obj['rules'])}.")


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data"""

    verbose = ctx.obj['verbose']
    if verbose:
        print('Running subcommand `run`.')
        print(f"Running in data directory {os.getcwd()}.")
        print(f"Using configuration:")
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    bad_patterns = ctx.obj['invalid_filename_patterns']
    global_rules = ctx.obj['globalrules']
    local_rules = ctx.obj['rules']
    rule_list = []
    if global_rules:
        if verbose:
            print(f"Reading global rule file {repr(global_rules)}.")
        rule_list.extend(parse_rules(global_rules, bad_patterns))
    if verbose:
        print(f"Reading local rule file {repr(global_rules)}.")
    # rule_list.extend(parse_rules(local_rules, bad_patterns))

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
