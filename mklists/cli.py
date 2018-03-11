import os
import sys
import posixpath

import click


class Config(object):

    def __init__(self, home):
        self.home = home
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s' % (key, value), file=sys.stderr)

    def __repr__(self):
        return '<Config %r>' % self.home


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.option('--list-folder', default='.', type=click.Path(exists=True),
              help='Changes the list folder location.')
@click.option('--config', nargs=2, multiple=True,
              metavar='KEY VALUE', help='Overrides a config key/value pair.')
@click.option('--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
@click.pass_context
def cli(ctx, list_folder, config, verbose):
    """Manage plain-text lists by tweaking rules
    """
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_config decorator.
    ctx.obj = Config(os.path.abspath(list_folder))
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@click.argument('src')
@click.argument('dest', required=False)
@click.option('--rev', '-r', default='HEAD',
              help='Clone a specific revision instead of HEAD.')
@pass_config
def clone(repo, src, dest, shallow, rev):
    """Initialize a list folder.

    Initializes directory with default configuration files:
    * '.rules' (mandatory)
    * '.mklistsrc' (expected but not mandatory)
    """
    if dest is None:
        dest = posixpath.split(src)[-1] or '.'
    click.echo('Cloning repo %s to %s' % (src, os.path.abspath(dest)))
    repo.home = dest
    if shallow:
        click.echo('Making shallow checkout')
    click.echo('Checking out revision %s' % rev)


@cli.command()
@click.option('--message', '-m', multiple=True,
              help='The commit message.  If provided multiple times each '
              'argument gets converted into a new line.')
@click.argument('files', nargs=-1, type=click.Path())
@pass_config
def commit(repo, files, message):
    """Commits outstanding changes.

    Commit changes to the given files into the repository.  You will need to
    "repo push" to push up your changes to other repositories.

    If a list of files is omitted, all changes reported by "repo status"
    will be committed.
    """
    if not message:
        marker = '# Files to be committed:'
        hint = ['', '', marker, '#']
        for file in files:
            hint.append('#   U %s' % file)
        message = click.edit('\n'.join(hint))
        if message is None:
            click.echo('Aborted!')
            return
        msg = message.split(marker)[0].rstrip()
        if not msg:
            click.echo('Aborted! Empty commit message')
            return
    else:
        msg = '\n'.join(message)
    click.echo('Files to be committed: %s' % (files,))
    click.echo('Commit message:\n' + msg)


@cli.command(short_help='Copies files.')
@click.option('--force', is_flag=True,
              help='forcibly copy over an existing managed file')
@click.argument('src', nargs=-1, type=click.Path())
@click.argument('dst', type=click.Path())
@pass_config
def copy(repo, src, dst, force):
    """Copies one or multiple files to a new location.  This copies all
    files from SRC to DST.
    """
    for fn in src:
        click.echo('Copy from %s -> %s' % (fn, dst))
