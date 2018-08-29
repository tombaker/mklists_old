@click.group()
@click.pass_context
def cli(ctx):

    if ctx.invoked_subcommand == 'init':
        click.echo(f"I was invoked with {ctx.invoked_subcommand}!!")
    if ctx.invoked_subcommand != 'init':
        click.echo(f"I was NOT invoked with init!!")

@cli.command()
@click.pass_context
def init(ctx):

    print(f"Running {ctx.invoked_subcommand}")

