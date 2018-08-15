"""docstring"""

from dataclasses import dataclass
from configparser import ConfigParser
import click
import sys
import yaml

# 1. Define Config class in module top level
# 2. Within group command function definition: 
#    * @click.pass_context 
#    * Function signature positional argument ('ctx')
#    * Instantiate Config object 
#    * Remember Config object as the context object ('ctx.obj')
#    * Save other 
# 5. In subcommands this point onwards other commands can refer to it by using the
# @pass_config decorator.


@click.group()
@click.option('--config', type=str, metavar='FILENAME', help="Configuration file.")
@click.option('--rules', type=str, metavar='FILENAME', multiple=True, help="Rule file, repeatable.")
@click.option('--data-folder', type=str, metavar='DIRNAME', help="Data folder.")
@click.option('--html-folder', type=str, metavar='DIRNAME', help="Data folder, urlified.")
@click.option('--backup-folder', type=str, metavar='DIRNAME', help="Backup folder.")
@click.option('--backup-depth', type=int, help="Backup depth.")
@click.option('--verbose', type=bool, is_flag=True, help="Run in verbose mode.")
@click.version_option('0.2', help="Show version and exit.")
@click.pass_context
def cli(ctx, config, rules, data_folder, html_folder, backup_folder, backup_depth, verbose):
    """Manage plain text lists by tweaking rules"""


    # Sensible default configuration values (eg, in absence of config file)
    ctx.obj = {
        'config': '.mklistsrc',
        'rules': ('.rules',),
        'data_folder': '.',
        'html_folder': '.html',
        'backup_folder': '.backups',
        'backup_depth': 3,
        'verbose': False}

    # if command line option points to different config file, use that one
    default_configfile_specified = True
    if config:
        ctx.obj['config'] = config
        default_configfile_specified = False

    # Confirm default config values
    print("Default config dict saved on ctx.obj = ", ctx.obj)  ################

    # Try to read configfile and use it to update ctx.obj
    # If configfile does not exist, write ctx.obj to a YAML file
    try:
        with open(config) as configfile:
            ctx.obj.update(yaml.load(configfile))
    except FileNotFoundError:
        if default_configfile_specified:
            print("Creating config file '.mklistsrc'. Can be edited.")
            yaml.safe_dump(ctx.obj, sys.stdout, default_flow_style=False)
        else:
            raise ConfigFileNotFoundError(f"{repr(config)} not found.")

    # if rules:
    #     ctx.obj['rules'] = rules

    # if data_folder:
    #     ctx.obj['data_folder'] = data_folder

    # if html_folder:
    #     ctx.obj['html_folder'] = html_folder

    # if backup_folder:
    #     ctx.obj['backup_folder'] = backup_folder

    if backup_depth:
        ctx.obj['backup_depth'] = backup_depth

    print("ctx.obj with backup_depth overriden by click option = ", ctx.obj)  ################

    # if verbose:
    #     ctx.obj['verbose'] = verbose

    # print("ctx.obj = ", ctx.obj)  ################ 12345
    # print("After overriding with values set on command line:"
    #       "ctx.obj['backup_depth'] =", repr(ctx.obj['backup_depth']))  #######

    # #click.echo(f'>>> ctx.obj.backup_depth      =>  {ctx.obj.backup_depth}') #####


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize folder for Mklists data."""
    print('@@@TODO')

@cli.command()
@click.pass_context
def make(ctx):
    """Regenerate lists according to rules."""
    click.echo(f'>>> ctx                             =>  {ctx}')
    click.echo(f'>>> ctx.obj                        =>  {ctx.obj}')
    click.echo(f'>>> ctx.obj["rules"]               =>  {ctx.obj["rules"]}')
    #click.echo(f'>>> ctx.list_folder               =>  {ctx.list_folder}')
    #click.echo(f'>>> ctx.backup_folder             =>  {ctx.backup_folder}')
    #click.echo(f'>>> ctx.backup_depth              =>  {ctx.backup_depth}')
    #click.echo(f'>>> ctx.html_folder               =>  {ctx.html_folder}')
    #click.echo(f'>>> ctx.verbose                   =>  {ctx.verbose}')
    #click.echo(f'>>> ctx.get_config                =>  {ctx.get_config}')
    #click.echo()

@cli.command()
@click.pass_context
def check(ctx):
    """Dry-run with verbose sanity checks."""
    print(f"mklists check: ctx.obj is {repr(ctx.obj)}")

@cli.command()
@click.pass_context
def rules(ctx):
    """Inspect rules."""
    # Print to screen all (non-dunder) config attributes/values

class ConfigFileNotFoundError(SystemExit):
    """Specified (non-default) configuration file was not found"""
