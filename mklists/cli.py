"""CLI - command-line interface module"""

import glob
import os
import sys
import click
import yaml
from mklists import (
    MKLISTSRC,
    STARTER_GLOBAL_RULEFILE,
    STARTER_LOCAL_RULEFILE,
    VALID_FILENAME_CHARS,
    ConfigFileNotFoundError,
    DatadirNotAccessibleError,
    InitError
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
    """Sync your plain-text todo lists to evolving rules"""

    # default settings (do valid_filename_characters need r prefix??)
    ctx.obj = {
        'globalrules': '.globalrules',
        'rules': '.rules',
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

    # override defaults with any settings specified in '.mklistsrc'
    try:
        with open(MKLISTSRC) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

    # override with any settings specified on command line
    def assign_to_ctxobj(context, context_object_key, value):
        if value:
            context.obj[context_object_key] = value

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

    if not os.path.exists(MKLISTSRC):
        print(f"Creating default {repr(MKLISTSRC)} - customize as needed.")
        with open(MKLISTSRC, 'w') as fout:
            yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)
    else:
        raise InitError(f"To re-initialize, first delete {repr(MKLISTSRC)}.")

    # Rules
    global_rulefile = ctx.obj['globalrules']
    if global_rulefile:
        if not os.path.exists(global_rulefile):
            print(f"Creating {global_rulefile} - tweak as needed.")
            with open(global_rulefile, 'w') as fout:
                fout.write(STARTER_GLOBAL_RULEFILE)
        else:
            print(f"Leaving pre-existing {repr(global_rulefile)} untouched.")

    local_rulefile = ctx.obj['rules']
    if not os.path.exists(local_rulefile):
        print(f"Creating {repr(local_rulefile)} - tweak as needed.")
        with open(local_rulefile, 'w') as fout:
            fout.write(STARTER_LOCAL_RULEFILE)
    else:
        print(f"Leaving pre-existing {repr(local_rulefile)} untouched.")


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files"""

    verbose = ctx.obj['verbose']
    valid_chars = ctx.obj['valid_filename_chars']
    invalid_patterns = ctx.obj['invalid_filename_patterns']
    global_rulefile = ctx.obj['globalrules']
    local_rulefile = ctx.obj['rules']
    rule_list = []
    if global_rulefile:
        if verbose:
            print(f"Reading global rule file {repr(global_rulefile)}.")
        grules = parse_rules(global_rulefile, 
                             good_chars=valid_chars, 
                             bad_pats=invalid_patterns)
        rule_list.extend(grules)
    if verbose:
        print(f"Reading local rule file {local_rulefile}.")
    lrules = parse_rules(local_rulefile, 
                         good_chars=valid_chars, 
                         bad_pats=invalid_patterns)
    rule_list.extend(lrules)
    if verbose:
        print(rule_list)

    visible_files = [name for name in glob.glob('*')]
    print(f"* get_datalines(ls={visible_files}, but_not=bad_patterns)")
    print(f"* Check data folder, verbosely.")

    print(f"* Get datalines from {visible_files}.")
    print(f"* Apply rules to datalines, modifying in-memory datadict.")
    print(f"* Backup option: Create time-stamped backup_dir.")
    print(f"* Backup option: Move existing files to backup_dir.")
    print(f"* Write out datadict values as files in datadir.")
    print(f"* HTML option: Write out datadict values as files in urlify_dir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")


@cli.command()
@click.pass_context
def debug(ctx):
    """Temporary subcommand for debugging purposes"""

    print('Running subcommand `debug`.')

    print(f"Global rules: {ctx.obj['globalrules']}")
    print(f"Local rules: {ctx.obj['rules']}")
    print(f"Default config: {MKLISTSRC}")
    sys.exit("Exiting")
