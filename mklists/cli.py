"""CLI - command-line interface module"""

import glob
import os
import sys
import click
import yaml
from mklists.datadir import get_datalines
from mklists.verbose import explain_configuration
from mklists.rules import parse_rules
from mklists import (
    MKLISTSRC,
    RULEFILE,
    STARTER_DEFAULTS,
    STARTER_GRULES,
    STARTER_LRULES,
    VALID_FILENAME_CHARS,
    ConfigFileNotFoundError,
    DatadirNotAccessibleError,
    InitError)


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
@click.option('--readonly', type=bool, is_flag=True, 
              help="Enable read-only mode")
@click.option('--verbose', type=bool, is_flag=True, 
              help="Enable verbose mode")
@click.version_option('0.1.4', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, globalrules, rules,
        backup, backup_dir, backup_depth,
        urlify, urlify_dir,
        readonly, verbose):
    """Sync your plain-text todo lists to evolving rules"""

    # If non-default datadir given on command line, change to that directory.
    if datadir is not None:
        try:
            os.chdir(datadir)
            if verbose:
                print(f"Changing to data directory {repr(datadir)}.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{datadir} is not accessible.")

    # Save default settings to object passed with @click.pass_context.
    ctx.obj = STARTER_DEFAULTS

    # Load mandatory MKLISTSRC, which may override default settings.
    # This step is skipped if mklists was invoked with subcommand 'init'.
    if ctx.invoked_subcommand != 'init':
        try:
            with open(MKLISTSRC) as configfile:
                ctx.obj.update(yaml.load(configfile))
        except FileNotFoundError:
            raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

    # Read settings specified on command line and use them to override.
    for key, value in [('globalrules', globalrules),
                       ('rules', rules),
                       ('urlify', urlify),
                       ('urlify_dir', urlify_dir),
                       ('backup', backup),
                       ('backup_dir', backup_dir),
                       ('backup_depth', backup_depth),
                       ('readonly', readonly),
                       ('verbose', verbose)]:
        if value is not None:
            ctx.obj[key] = value

    # Show detailed explanation of current settings resulting from the above.
    if verbose:
        explain_configuration(**ctx.obj)

@cli.command()
@click.pass_context
def init(ctx):
    """Generate default configuration and rule files"""

    # If MKLISTSRC already exists, exit with advice.
    # If MKLISTSRC not found, create and populate with current settings.
    # Note: If 'readyonly' specified, will not actually write to disk.
    if os.path.exists(MKLISTSRC):
        raise InitError(f"To re-initialize, first delete {repr(MKLISTSRC)}.")
    else:
        if ctx.obj['readonly']:
            print(f"READONLY: would have created {repr(MKLISTSRC)}.")
        else:
            print(f"Creating default {repr(MKLISTSRC)} - customize as needed.")
            with open(MKLISTSRC, 'w') as fout:
                yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)


    # Look for global and local rule files named in settings.
    # If local rule file was not named anywhere (edge case), call it RULEFILE.
    # If either or both files already exist (atypical), leave them untouched.
    # Otherwise, create one or both rule files with default contents.
    # Note: If 'readyonly' specified, will not actually write to disk.
    if not ctx.obj['rules']:   
        ctx.obj['rules'] = RULEFILE
    for file, content in [(ctx.obj['globalrules'], STARTER_GRULES),
                          (ctx.obj['rules'], STARTER_LRULES)]:
        if file:
            if os.path.exists(file):
                print(f"Found {repr(file)} - leaving untouched.")
            else:
                if ctx.obj['readonly']:
                    print(f"READONLY: would have created {repr(file)}.")
                else:
                    print(f"Creating {repr(file)} - tweak as needed.")
                    with open(file, 'w') as fout:
                        fout.write(content)


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files"""

    ls_visible = [name for name in glob.glob('*')]
    verbose = ctx.obj['verbose']
    grules = ctx.obj['globalrules']
    lrules = ctx.obj['rules']
    good = ctx.obj['valid_filename_characters']
    bad = ctx.obj['invalid_filename_patterns']

    #print(repr(grules))
    #print(repr(lrules))

    readonly = True # 2018-08-31: for purposes of testing
    verbose = True  # 2018-08-31: for purposes of testing

    # Read rule files (if they exist) and parse.
    rule_object_list = []
    for rulefile in grules, lrules:
        if rulefile:
            print(rulefile)
            rule_object_list.extend(parse_rules(rulefile, good_chars=good))
        if not rule_object_list:
            print("No rules to work with!") # turn this into exception
        if verbose: # just for debugging
            for rule in rule_object_list:
                print(rule)
            
    # Check data directory ('.') and get aggregated list of data lines.
    data_lines = get_datalines(ls=ls_visible, but_not=bad)
    print(data_lines)

    #for dir in dirs[3:]:
    #    print(f"del {directory}")
    #hashlib.sha224(datalines.encode('utf-8')).hexdigest()
    #import hashlib
    #hashlib.sha224(''.join(sorted(datalines)).encode('utf-8')).hexdigest()

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
    for item in ctx.__dir__():
        print(item)
