import click
from mklists.cli import *

@cli.command()
@click.pass_context
def debug(ctx):
    """Temporary subcommand for debugging purposes"""

    print('Running subcommand `debug`.')
    for item in ctx.__dir__():
        print(item)
