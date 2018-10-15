"""CLI - command-line interface module"""

import glob
import click
from mklists.utils import change_working_directory
from mklists.readwrite import (
    apply_rules_to_datalines,
    load_mklistsrc,
    write_initial_configfile,
    write_initial_rulefiles,
    get_rules,
    get_datalines,
    write_urlified_datafiles
    )
from mklists.verbose import explain
from mklists import (
    MKLISTSRC,
    RULEFILE,
    STARTER_DEFAULTS,
    ConfigFileNotFoundError,
    DatadirNotAccessibleError,
    NoDataError)


@click.group()
@click.option('--datadir', type=str, metavar='DIRPATH',
              help="Use DIRPATH as working directory [./]")
@click.option('--globalrules', type=str, metavar='FILEPATH',
              help="Set non-default global rules [./.globalrules]")
@click.option('--rules', type=str, metavar='FILEPATH',
              help="Set non-default local rules [./.rules]")
@click.option('--backup', type=bool, is_flag=True,
              help="Enable backup of input data [./.backups/]")
@click.option('--backup-dir', type=str, metavar='DIRPATH',
              help="Set non-default directory for backups")
@click.option('--backup-depth', type=int, metavar='INTEGER',
              help="Set number of backups to keep [3]")
@click.option('--urlify', type=bool, is_flag=True,
              help="Enable HTML copies of output files [./.html/]")
@click.option('--urlify-dir', type=str, metavar='DIRPATH',
              help="Set non-default directory for HTML data")
@click.option('--readonly', type=bool, is_flag=True,
              help="Enable read-only mode")
@click.option('--verbose', type=bool, is_flag=True,
              help="Enable verbose mode")
@click.version_option('0.1.4', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, datadir, globalrules, rules, backup, backup_dir, backup_depth,
        urlify, urlify_dir, readonly, verbose):
    """Sync your plain-text todo lists to evolving rules"""

    # "Untoucable" dictionary of cli() parameters snapshotted as mutable dict.
    cliargs = locals()

    # If non-default datadir given on command line, change to that directory.
    # If directory is not accessible, exit with error message.
    change_working_directory(datadir, verb=verbose)

    # Save default settings to object to be passed with @click.pass_context.
    ctx.obj = STARTER_DEFAULTS

    # Load config file MKLISTSRC, overriding some settings in context object.
    # -- If MKLISTSRC not found, terminates with advice to run `mklists init`.
    # -- If `mklists` was invoked with subcommand 'init', this step is skipped.
    if ctx.invoked_subcommand != 'init':
        load_mklistsrc(MKLISTSRC, context=ctx.obj, verbose=ctx.obj['verbose'])

    # Save settings specified on command line ("not None") to context object.
    # -- Omits 'ctx', the context object itself.
    # -- Omits 'datadir', used just once so not saved on context object.
    for item in cliargs:
        if item != 'ctx' and item != 'datadir' and cliargs[item] is not None:
            ctx.obj[item] = cliargs[item]

    # Show detailed exposition of current settings resulting from the above.
    if verbose:
        explain(**ctx.obj)


@cli.command()
@click.pass_context
def init(ctx):
    """Generate default configuration and rule files"""

    # If configfile already exists, exit suggesting to delete it first.
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
    # -- Does not complain or exit if rules are empty @@@CHECK
    rules = get_rules(grules=ctx.obj['globalrules'],
                      lrules=ctx.obj['rules'],
                      valid_filename_chars=ctx.obj['valid_filename_chars'],
                      verbose=ctx.obj['verbose'])

    # Get aggregated list of lines from files in working directory.
    datalines = get_datalines(ls_visible=[name for name in glob.glob('*')],
                              but_not=ctx.obj['invalid_filename_patterns'],
                              verbose=ctx.obj['verbose'])

    # Apply rules to datalines (loads and modifies in-memory data dictionary).
    # -- Exits with message if 'rules_list' or 'datalines_list' are empty.
    mklists_dict = apply_rules_to_datalines(rules_list=rules,
                                              datalines_list=datalines)

    # If 'backup' is ON:
    # before writing mklists_dict contents to disk,
    # creates timestamped backup directory in specified backup_dir,
    # and moves all visible files in data directory to backup directory.
    if ctx.obj['backup']:
        move_datafiles_to_backup(ls_visible=[name for name in glob.glob('*')],
                                 backup=True,   # 2018-09-02: just for now?
                                 backup_dir=ctx.obj['backup_dir'],
                                 backup_depth=ctx.obj['backup_depth'])

    # If 'backup' is ON, move existing files from working to backup directory.
    # If 'backup' is OFF, DELETE existing files in working directory.
    # Write mklists_dict to working directory: 
    # -- mklists_dict keys are names of files.
    # -- mklists_dict values are contents of files.
    # -- If 'readonly' is ON, will only print messages, not write to disk.
    write_new_datafiles(datalines_d=mklists_dict,
                        readonly=True,  # later: ctx.obj['readonly'],
                        verbose=ctx.obj['verbose'])

    # If 'urlify' is ON, write urlified data files to urlify_dir.
    if ctx.obj['urlify']:
        write_urlified_datafiles(datalines_d=mklists_dict,
                                 urlify_dir=ctx.obj['urlify_dir'],
                                 urlify_depth=ctx.obj['urlify_depth'],
                                 readonly=True,  # later: ctx.obj['readonly'],
                                 verbose=ctx.obj['verbose'])

    # If 'files2dirs' is ON, settable only in MKLISTSRC (not on command line),
    # move selected files to external directories.
    if ctx.obj['files2dirs']:
        move_files_to_external_directories(files2dirs_dict=ctx.obj['files2dirs'])
