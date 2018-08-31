"""CLI - command-line interface module"""

import glob
import os
import click
import yaml
from mklists.utils import (
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

    # If configfile already exists, exit with advice.
    # If configfile not found, create new file, populate with current settings.
    # Note: if 'readonly' specified, will only print messages to screen.
    write_initial_configfile(filename=MKLISTSRC)

    # Look for global and local rule files named in settings.
    # -- If local rule file not named in settings, call it RULEFILE.
    # -- If either or both files already exist (atypical), leave untouched.
    # Create one or both rule files with default contents.
    # Note: If 'readyonly' specified, will not actually write to disk.
    write_initial_rulefiles(grules=None, lrules=RULEFILE)


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files"""

    verbose = True  # 2018-08-31: for purposes of testing

    visible_things = [name for name in glob.glob('*')]

    # Read rule files (if they exist) and parse.
    rules = get_rules(grules=ctx.obj['globalrules'],
                      lrules=ctx.obj['rules'],
                      good_chars=ctx.obj['valid_filename_chars'])
    if verbose:   # just for debugging
        for rule in rules:
            print(rule)

    # In current directory, get aggregated list of data lines.
    datalines = []
    for thing in visible_things:
        datalines.append(get_lines(thing))
    if verbose:   # just for debugging
        print(datalines)
    if not datalines:
        raise NoDataError('No data to process!')

    print(f"* Apply rules to datalines, modifying in-memory datadict.")
    print(f"* Backup option: Create time-stamped backup_dir.")
    print(f"* Backup option: Move existing files to backup_dir.")
    print(f"* Write out datadict values as files in datadir.")
    print(f"* HTML option: Write out datadict values as files in urlify_dir.")
    print(f"* Move files outside datadir as per ['files2dirs'].")

    # Ideas:
    #    for dir in dirs[3:]:
    #        print(f"del {directory}")
    #    hashlib.sha224(datalines.encode('utf-8')).hexdigest()
    #    import hashlib
    #    hashlib.sha224(''.join(sorted(datalines)).encode('utf-8')).hexdigest()


@cli.command()
@click.pass_context
def debug(ctx):
    """Temporary subcommand for debugging purposes"""

    print('Running subcommand `debug`.')
    for item in ctx.__dir__():
        print(item)
