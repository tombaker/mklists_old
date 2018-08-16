from dataclasses import dataclass
from configparser import ConfigParser
import click
import sys
import yaml

@click.group()
@click.option('--config', type=str, metavar='FILENAME', 
              help="Config file [.mklistsrc]")
@click.option('--rules', type=str, metavar='FILENAME', multiple=True, 
              help="Rule file - repeatable [.rules]")
@click.option('--data', type=str, metavar='DIRNAME', 
              help="Data folder [.]")
@click.option('--html', type=str, metavar='DIRNAME', 
              help="Data folder, urlified [.html]")
@click.option('--backups', type=str, metavar='DIRNAME', 
              help="Backup folder [.backups]")
@click.option('--backup-depth', type=int, metavar='INT',
              help="Backup depth [3]")
@click.option('--verbose', type=bool, is_flag=True, 
              help="Run verbosely")
@click.version_option('0.1.1', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, config, rules, data, html, backups, 
        backup_depth, verbose):
    """Manage plain text lists by tweaking rules"""

    if verbose:
        print('Printing diagnostic information.')

    # Hardwired config values (before reading optional config file)
    ctx.obj = {
        'config': '.mklistsrc',
        'rules': ['.rules',],
        'data': '.',
        'html': '.html',
        'backups': '.backups',
        'backup_depth': 3,
        'verbose': False}

    if verbose:
        click.echo('Hardwired config defaults:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # If command line specifies non-default config file, use it
    if config:
        using_nondefault_configfile = True
        ctx.obj['config'] = config
        if verbose:
            print(f"Will use config file, {repr(ctx.obj['config'])}.")
    else:
        using_nondefault_configfile = False

    # Try to read configfile and use it to update ctx.obj
    # If configfile does not exist, write ctx.obj to a YAML file
    try:
        with open(ctx.obj['config']) as configfile:
            ctx.obj.update(yaml.load(configfile))
        if verbose:
            print('Config settings after reading config file:')
            for key, value in ctx.obj.items():
                print("    ", key, "=", value)
    except FileNotFoundError:
        if using_nondefault_configfile:
            raise ConfigFileNotFoundError(f"File {repr(config)} not found.")
        else:
            print("Warning: No config file found; using hardwired defaults.")

    if rules:
        ctx.obj['rules'] = list(rules)
        if verbose:
            print(f"Will use rule file(s) {repr(ctx.obj['rules'])}.")

    if data:
        ctx.obj['data'] = data
        if verbose:
            print(f"Will use data folder {repr(ctx.obj['data'])}.")

    if html:
        ctx.obj['html'] = html
        if verbose:
            print(f"Will use urlified data folder {repr(ctx.obj['html'])}.")

    if backups:
        ctx.obj['backups'] = backups
        if verbose:
            print(f"Will use backups folder {repr(ctx.obj['html'])}.")

    if backup_depth:
        ctx.obj['backup_depth'] = backup_depth
        if verbose:
            print(f"Will keep last {repr(ctx.obj['backup_depth'])} backups.")

    if verbose:
        ctx.obj['verbose'] = verbose
        print('Final config settings:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

@cli.command()
@click.pass_context
def init(ctx):
    """Initialize data folder"""

    print(f"Creating mandatory default rule file: '.rules'.")
    print(f"Creating optional config file {repr(ctx.obj['config'])}.")
    # yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)

@cli.command()
@click.pass_context
def make(ctx):
    """Remake lists as per rules"""

    print(f"* Get rules: {repr(ctx.obj['rules'])}.")
    print(f"* Check data folder: {repr(ctx.obj['data'])}.")
    print(f"* Get data: {repr(ctx.obj['data'])}.")
    print(f"* Apply rules to data, modifying data dictionary.")
    print(f"* Double-check for data loss??")
    print(f"* Create (or use) time-stamped folder within backup folder.")
    print(f"* Move files to time-stamped backup folder.")
    print(f"* Write out data dictionary as files in data folder.")

@cli.command()
@click.pass_context
def verify(ctx):
    """Check rules and data folder, verbosely"""

    print(f"* Get rules: {repr(ctx.obj['rules'])}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['data'])}, verbosely.")


class ConfigFileNotFoundError(SystemExit):
    """Specified (non-default) configuration file was not found"""
