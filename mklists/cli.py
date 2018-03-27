import os
import sys

import click
from dataclasses import dataclass

print('Running mklists')
print()
print()


class ListFolder():

    def __init__(self, cwd):
        self.cwd = cwd
        self.config = {}
        self.verbose = False

    def get_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo('running verbose')

    def __repr__(self):
        return '<ListFolder %r>' % self.cwd


pass_config = click.make_pass_decorator(ListFolder)


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
              help='Compares summed size before and after.')
@click.option('--verbose', is_flag=True,
              help='Enable verbose mode.')
@click.version_option('0.1')
@click.pass_context
def cli(ctx, list_folder, backup_folder, html_folder, config, rules, verbose):
    """Rearrange plain-text lists by tweaking rules
    """
    ctx.obj = ListFolder(os.path.abspath(list_folder))
    ctx.obj.verbose = verbose


@cli.command()
@pass_config
def init(list_folder):
    """Initialize list folder.

    Initializes directory with default configuration files:
    * '.rules' (mandatory)
    * '.mklistsrc' (expected but not mandatory)
    """


@cli.command()
@click.option('--backup-depth', default=3, 
              help='Retains max number of backups [3].')
@pass_config
def run(repo, backup_depth):
    """Remake lists.
    """


@cli.command()
@pass_config
def check(ctx, files, message):
    """Dry-run with verbose sanity checks.
    """

