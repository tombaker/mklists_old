"""CLI - command-line interface module"""

import glob
import os
import click
import yaml
from mklists.utils import (
    set_data_directory,
    load_mklistsrc,
    write_initial_configfile,
    write_initial_rulefiles,
    get_rules,
    get_lines,
    )
from mklists.verbose import explain_configuration
from mklists import (
    MKLISTSRC,
    RULEFILE,
    STARTER_DEFAULTS,
    ConfigFileNotFoundError,
    DatadirNotAccessibleError,
    NoDataError)
from mklists.shuffle import apply_rules_to_datalines


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

    # Save dictionary of arguments passed on the command line.
    cliargs = locals()

    # If non-default datadir given on command line, change to that directory.
    # If directory is not accessible, exit with error message.
    set_data_directory(datadir)

    # Save default settings to object passed with @click.pass_context.
    ctx.obj = STARTER_DEFAULTS

    # Load mandatory file MKLISTSRC, overriding some or all default settings.
    # -- This step is skipped if mklists was invoked with subcommand 'init'.
    if ctx.invoked_subcommand != 'init':
        load_mklistsrc(MKLISTSRC, context=ctx.obj, verbose=ctx.obj['verbose'])

    # Save settings specified on command line ("not None") to context object.
    # -- Exception: 'ctx' - the context object itself.
    # -- Exception: 'datadir' - used once and not saved on context object.
    for item in cliargs:
        if item != 'ctx' and item != 'datadir' and cliargs[item] is not None:
            ctx.obj[item] = cliargs[item]

    # Show detailed exposition of current settings resulting from the above.
    if verbose:
        explain_configuration(**ctx.obj)


@cli.command()
@click.pass_context
def init(ctx):
    """Generate default configuration and rule files"""

    # If configfile already exists, exit with advice.
    # If configfile not found, create new file using current settings.
    # Note: if 'readonly' is ON, will only print messages, not write to disk.
    write_initial_configfile(context=ctx.obj,
                             filename=MKLISTSRC, 
                             readonly=True, # later: ctx.obj['readonly'],
                             verbose=ctx.obj['verbose'])

    # Look for global and local rule files named in settings.
    # -- If local rule file not named in settings, call it RULEFILE.
    # -- If either or both files already exist (atypical), leave untouched.
    # Create one or both rule files with default contents.
    # Note: if 'readonly' is ON, will only print messages, not write to disk.
    write_initial_rulefiles(grules=None, 
                            lrules=RULEFILE, 
                            readonly=True, # later: ctx.obj['readonly'],
                            verbose=ctx.obj['verbose'])


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files"""
    # Read rule files, parse, and get aggregated list of rules objects.
    rules = get_rules(grules=ctx.obj['globalrules'],
                      lrules=ctx.obj['rules'],
                      valid_filename_chars=ctx.obj['valid_filename_chars'],
                      verbose=ctx.obj['verbose'])

    # In current directory, get aggregated list of data lines.
    datalines = get_datalines(ls_visible=[name for name in glob.glob('*')],
                              but_not=ctx.obj['invalid_filename_patterns'],
                              verbose=ctx.obj['verbose'])

    # Apply rules to datalines (loads and modifies in-memory data dictionary).
    datalines_dict = apply_rules_to_datalines(rules_list=rules,
                                              datalines_list=datalines)

    # If 'backup' is ON: 
    # before writing datalines_dict contents to disk, 
    # creates timestamped backup directory in specified backup_dir,
    # and moves all visible files in data directory to backup directory.
    if ctx.obj['backup']:
        move_datafiles_to_backup(ls_visible=[name for name in glob.glob('*')],
                                 backup=True,   # 2018-09-02: just for now?
                                 backup_dir=ctx.obj['backup_dir'],
                                 backup_depth=ctx.obj['backup_depth'])

    # Write out items in datalines_dict: 
    # -- files named for dictionary keys, 
    # -- file contents are dictionary values.
    # Note: if 'readonly' is ON, will only print messages, not write to disk.
    # Note: if 'backup' is ON, will move existing data to backup directory.
    write_new_datafiles_to_disk(datalines_d=datalines_dict,
                                readonly=True,  # later: ctx.obj['readonly'],
                                verbose=ctx.obj['verbose'])

    print("2018-09-02: remains to be done:")
    print(f"* Backup option: Create time-stamped backup_dir.")
    print(f"* Backup option: Move existing files to backup_dir.")
    print(f"* HTML option: Write out datadict values as files in urlify_dir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")
