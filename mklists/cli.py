import os
import re
import sys
import glob

import click
from posixpath import realpath
from dataclasses import dataclass
from configparser import ConfigParser

class ListFolder:

    def __init__(*kwargs):
        pass

    def ls_visible_files(folder='.'):
        visible_files = [name for name in glob.glob('*') if os.path.isfile[name]]
        return visible_files


@click.group()
@click.option('--config', default='.mklistsrc', type=click.File('r'),
              help="Change config file [.mklistsrc].")
@click.option('--rules', default='.rules', type=click.File('r'),
              help="Change local rules [.rules]. Repeatable.")
@click.option('--list-folder', default='.',
              type=click.Path(exists=True),
              help="Change list folder [./].")
@click.option('--backup-folder', default='.backups',
              type=click.Path(),
              help="Change backup folder [.backups/].")
@click.option('--backup-depth', type=click.INT,
              help="Change backup depth [3].")
@click.option('--html-folder', default='.sgml', type=click.Path(),
              help="Set urlified-lists folder [None].")
@click.option('--verbose', default=False, is_flag=True,
              help='Enable verbose mode.')
@click.version_option('0.2')
@click.pass_context
def cli(ctx, 
        config, rules,
        list_folder, backup_folder, backup_depth, html_folder, 
        verbose):
    """Rearrange plain-text to-do lists by tweaking rules"""
    config_parser = ConfigParser()
    config_parser.read('.mklistsrc')
    mklistsrc = dict([[key, config_parser['DEFAULTS'][key]] for key in config_parser['DEFAULTS']])
    print("mklistsrc = ", mklistsrc)
    ctx.obj = mklistsrc
    print("ctx.obj = ", ctx.obj)

#    if list_folder:   ctx.obj['list_folder'] = list_folder
#    if backup_folder: ctx.obj['backup_folder'] = backup_folder
#    if backup_depth:  ctx.obj['backup_depth'] = backup_depth
#    print(ctx.obj)
#    if html_folder:   ctx.obj['html_folder'] = html_folder
#    if config:        ctx.obj['config'] = config
#    if rules:         ctx.obj['rules'] = rules
#    if global_rules:  ctx.obj['global_rules'] = global_rules
#    if verbose:       ctx.obj['verbose'] = verbose
#
#    click.echo(f'>>> cli                       =>  {cli}')
#    click.echo(f'>>> ctx.obj.__dir__()...      =>  {[item for item in ctx.obj.__dir__() if not re.search("__", item)]}')
#    click.echo(f'>>> ctx.obj.list_folder       =>  {ctx.obj.list_folder}')
#    click.echo(f'>>> ctx.obj.backup_folder     =>  {ctx.obj.backup_folder}')
#    click.echo(f'>>> ctx.obj.backup_depth      =>  {ctx.obj.backup_depth}')
#    click.echo(f'>>> ctx.obj.html_folder       =>  {ctx.obj.html_folder}')
#    click.echo(f'>>> ctx.obj.config            =>  {ctx.obj.config}')
#    click.echo(f'>>> ctx.obj.rules             =>  {ctx.obj.rules}')
#    click.echo(f'>>> ctx.obj.global_rules      =>  {ctx.obj.global_rules}')
#    click.echo(f'>>> ctx.obj.verbose           =>  {ctx.obj.verbose}')
#    click.echo(f'>>> ctx.obj.get_config        =>  {ctx.obj.get_config}')
#    click.echo()


# ----------------------------------------------------------------------
@cli.command()
@click.pass_context
def init(list_folder):
    """Initialize list folder."""
    print('@@@TODO')

# ----------------------------------------------------------------------
@cli.command()
@click.pass_context
def run(cli):
    """Regenerate lists according to rules."""
    click.echo(f'>>> cli                             =>  {cli}')
    click.echo(f'>>> cli.obj                        =>  {cli.obj}')
    click.echo(f'>>> cli.obj["rules"]               =>  {cli.obj["rules"]}')
    #click.echo(f'>>> cli.__dir__()...              =>  {[item for item in cli.__dir__() if not re.search("__", item)]}')
    #click.echo(f'>>> cli.list_folder               =>  {cli.list_folder}')
    #click.echo(f'>>> cli.backup_folder             =>  {cli.backup_folder}')
    #click.echo(f'>>> cli.backup_depth              =>  {cli.backup_depth}')
    #click.echo(f'>>> cli.html_folder               =>  {cli.html_folder}')
    #click.echo(f'>>> cli.verbose                   =>  {cli.verbose}')
    #click.echo(f'>>> cli.get_config                =>  {cli.get_config}')
    #click.echo()

# ----------------------------------------------------------------------
@cli.command()
@click.pass_context
def check(ctx):
    """Dry-run with verbose sanity checks.
    """
    # Print to screen all (non-dunder) config attributes/values


# ======================================================================
@dataclass
class RuleSet():

    def get_rules():
        """Read rules file, return rule set."""

# ======================================================================
@dataclass 
class ListFile():
    file = click.Path
    # is_utf8_encoded()
    # file has legal name (only allowable characters - e.g., no spaces)
    # is_text (implement this?)
    #   allowable_percent_non_ascii_characters
    #   return True or False
    # return { file: [['one line\n'], [...]] }
