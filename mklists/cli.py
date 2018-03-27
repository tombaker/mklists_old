import os
import re
import sys

import click
from dataclasses import dataclass
from posixpath import realpath

@dataclass
class ListFolder():
    list_folder:       click.Path
    backup_folder:     click.Path = '.mklists'
    backup_depth:      int = 3
    html_folder:       click.Path = '.html'
    config:            click.File = '.mklistsrc'
    rules:             click.File = '.rules'
    with_verification: bool = True 
    verbose:           bool = False

    def get_config(self):
        click.echo('@@@ get configuration')
        if self.verbose:
            click.echo('running verbose')

pass_listfolder = click.make_pass_decorator(ListFolder)


@click.group()
@click.option('--list-folder', default='.', 
              type=click.Path(exists=True),
              help="Change list folder [./].")
@click.option('--backup-folder', default='.mklists', 
              type=click.Path(),
              help="Change backup folder [.mklists/].")
@click.option('--backup-depth', default=3, 
              help="Change backup depth [3].")
@click.option('--html-folder', default='.html', 
              type=click.Path(),
              help="Set urlified-lists folder [None].")
@click.option('--config', default='.mklistsrc', 
              type=click.File('r'),
              help="Change config file [.mklistsrc].")
@click.option('--rules', default='.rules', # multiple=True, 
              type=click.File('r'),
              help="Change rules [.rules]. Repeatable.")
@click.option('--with-verification', is_flag=True,
              help='Compare before size with after [True].')
@click.option('--verbose', is_flag=True,
              help='Enable verbose mode.')
@click.version_option('0.1')
@click.pass_context
def cli(ctx, list_folder, backup_folder, backup_depth, html_folder, config, rules, with_verification, verbose):
    """Rearrange plain-text lists by tweaking rules
    """
    ctx.obj = ListFolder(os.path.abspath(list_folder))
    ctx.obj.verbose = verbose

    click.echo(f'cli()                      {cli}')
    click.echo(f'ctx.obj.__dir__()...       {[item for item in ctx.obj.__dir__() if not re.search("__", item)]}')
    click.echo(f'ctx.obj.list_folder        {ctx.obj.list_folder}')
    click.echo(f'ctx.obj.backup_folder      {ctx.obj.backup_folder}')
    click.echo(f'ctx.obj.backup_depth       {ctx.obj.backup_depth}')
    click.echo(f'ctx.obj.html_folder        {ctx.obj.html_folder}')
    click.echo(f'ctx.obj.config             {ctx.obj.config}')
    click.echo(f'ctx.obj.rules              {ctx.obj.rules}')
    click.echo(f'ctx.obj.with_verification  {ctx.obj.with_verification}')
    click.echo(f'ctx.obj.verbose            {ctx.obj.verbose}')
    click.echo(f'ctx.obj.get_config         {ctx.obj.get_config}')
    click.echo()


@cli.command()
@pass_listfolder
def init(list_folder):
    """Initialize list folder.

    Initializes directory with default configuration files:
    * '.rules' (mandatory)
    * '.mklistsrc' (expected but not mandatory)
    """


@cli.command()
@click.option('--backup-depth', default=3, 
              help='Retains max number of backups [3].')
@pass_listfolder
def run(repo, backup_depth):
    """Remake lists.
    """


@cli.command()
@pass_listfolder
def check(ctx):
    """Dry-run with verbose sanity checks.
    """

