import os
import sys

import click


class Config():

    def __init__(self, cwd):
        self.cwd = cwd
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s' % (key, value), file=sys.stderr)

    def __repr__(self):
        return '<Config %r>' % self.cwd


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.option('--list-folder', default='.', type=click.Path(exists=True),
              help='Changes list folder location.')
@click.option('--config', default='.mklists.yaml', type=click.Path(exists=True),
              help='Changes configuration file; repeatable.')
@click.option('--rules', default='.rules', multiple=True, type=click.Path(exists=True),
              help='Changes file file; repeatable.')
@click.option('--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
@click.pass_context
def cli(ctx, list_folder, config, rules, verbose):
    """Manage plain-text lists by tweaking rules
    """
    ctx.obj = Config(os.path.abspath(list_folder))
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@pass_config
def init(list_folder):
    """Initialize current folder as new list folder.

    Initializes directory with default configuration files:
    * '.rules' (mandatory)
    * '.mklistsrc' (expected but not mandatory)
    """


@cli.command()
@pass_config
def mklists(repo, files, message):
    """Remake lists in list folder.
    """


@cli.command()
@pass_config
def check(ctx, files, message):
    """Check list folder and report problems.
    """

@cli.command(short_help='Backs up list directory.')
@click.argument('target', type=click.Path())
@pass_config
def backup(repo, target):
    """Back up list directory to time-stamped directory.
    """
    for fn in src:
        click.echo('Copy from %s -> %s' % (fn, dst))
