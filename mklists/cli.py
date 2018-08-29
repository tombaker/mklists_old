"""CLI - command-line interface module"""

import glob
import os
import sys
import click
import yaml
from mklists.rules import parse_rules
from mklists import (
    MKLISTSRC,
    STARTER_GLOBAL_RULEFILE,
    STARTER_LOCAL_RULEFILE,
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

    # 2018-08-29: This should provide way to call an init _module_
    # Also: make anki cards
    if ctx.invoked_subcommand == 'init':
        click.echo(f"I was invoked with {ctx.invoked_subcommand}!!")
    if ctx.invoked_subcommand != 'init':
        click.echo(f"I was NOT invoked with {ctx.invoked_subcommand}!!")

    # If non-default datadir given on command line, change to that directory.
    if datadir is not None:
        try:
            os.chdir(datadir)
            if verbose:
                print(f"Setting {repr(datadir)} as current data directory.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{datadir} is not accessible.")

    # Save hardwired default settings to object passed with @pass_context.
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
        'invalid_filename_patterns': [r'\.swp$', r'\.tmp$', r'~$', r'^\.'],
        'files2dirs': None}

    # Override default settings with any settings loaded from '.mklistsrc'.
    # Oops - if MKLISTSRC does not exist, exits before `init` can fire.
    try:
        with open(MKLISTSRC) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

    # Override settings with settings explicitly specified on command line.
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

    # If user asked for 'verbose', tell user what should happen now.
    if verbose:
        if ctx.obj['globalrules']:
            print(f"Using global rule file {ctx.obj['globalrules']}.")
        else:
            print("No global rule file found")

        if ctx.obj['rules']:
            print(f"Using global rule file {ctx.obj['rules']}.")
        else:
            print("Uh-oh - no rule file found")

        if ctx.obj['urlify']:
            print(f"Will convert copies of TXT files into HTML.")
        else:
            print(f"Will NOT convert copies of TXT files into HTML.")

        if ctx.obj['urlify_dir']:
            print(f"If urlify activated, files saved in {ctx.obj['urlify']}.")
        else:
            print(f"If urlify activated, would fail: no destination dir.")

        if backup:
            print("Will back up data files")
        else:
            print("Will not back up data files")

        if backup_dir:
            # Somewhere in module, calculate YYYYMMDD
            print("Will back up files to directory X/YYYYMMDD_hhmmss")

        if backup_depth:
            print("Will keep last {backup_depth} backups.")

        if readonly:
            print("Will stop short of writing to disk or moving files.")

        if valid_filename_characters:
            print("Filenames must consist only of the following characters:")
            print(f"{valid_filename_chars}")

        if files2dirs:
            print("Output file of given name to be moved to given directory.")

        print("Edit MKLISTSRC to change settings for future use")




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

    if not ctx.obj['rules']:   # hopefully a rare edge case
        raise InitError(f"Filename needed for local rule file (eg, '.rules').")

    for file, content in [(ctx.obj['globalrules'], STARTER_GLOBAL_RULEFILE),
                          (ctx.obj['rules'], STARTER_LOCAL_RULEFILE)]:
        if file:
            if not os.path.exists(file):
                print(f"Creating {file} - tweak as needed.")
                with open(file, 'w') as fout:
                    fout.write(content)
            else:
                print(f"Found {repr(file)} - leaving untouched.")


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
    print(f"Parent context is {ctx.parent.__dir__()}")
    print('=====')
    print(f"Parent command is {ctx.parent.command.__dir__()}")
    print('=====')
    print(f"Parent invoked command is {ctx.parent.invoked_subcommand}")

    print(f"Global rules: {ctx.obj['globalrules']}")
    print(f"Local rules: {ctx.obj['rules']}")
    print(f"Default config: {MKLISTSRC}")

    show_context(**ctx.obj)

    sys.exit("Exiting")

# Next - try moving to another module
def show_context(**kwargs):
    print(kwargs)
