import os
import sys

import click

print('Running mklists')
print()
print()


class ListFolder():

    def __init__(self, cwd):
        self.cwd = cwd
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s' % (key, value), file=sys.stderr)

    def __repr__(self):
        return '<ListFolder %r>' % self.cwd


pass_config = click.make_pass_decorator(ListFolder)


@click.group()
@click.option('--list-folder', 
              default='.', 
              type=click.Path(exists=True),
              help="Change list folder [./].")
@click.option('--backup-folder', 
              default='.mklists', 
              type=click.Path(),
              help="Change backup folder [.mklists/].")
@click.option('--config', 
              default='.mklistsrc', 
              type=click.Path(exists=True),
              help="Change config file [.mklistsrc].")
@click.option('--rules', 
              default='.rules', 
              multiple=True, 
              # type=click.Path(exists=True),
              help="Change rules [.rules]. Repeatable.")
@click.option('--verbose', is_flag=True,
              help='Enable verbose mode.')
@click.version_option('0.1')
@click.pass_context
def cli(ctx, list_folder, config, rules, verbose):
    """Rearrange plain-text lists by tweaking rules
    """
    ctx.obj = ListFolder(os.path.abspath(list_folder))
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@pass_config
def init(list_folder):
    """Initialize list folder.

    Initializes directory with default configuration files:
    * '.rules' (mandatory)
    * '.mklistsrc' (expected but not mandatory)
    """


@cli.command()
@pass_config
def run(repo, files, message):
    """Remake lists.
    """


@cli.command()
@pass_config
def check(ctx, files, message):
    """Dry-run with verbose sanity checks.
    """

@cli.command()
@click.argument('target', type=click.Path())
@pass_config
def checkpoint(repo, target):
    """Snapshot lists to backup folder.
    """
    for fn in src:
        click.echo('Copy from %s -> %s' % (fn, dst))
