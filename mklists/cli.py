"""CLI - command-line interface module"""

import yaml
import click


@click.group()
@click.option('--config', type=str, metavar='FILENAME',
              help="Config file [.mklistsrc]")
@click.option('--rules', type=str, metavar='FILENAME', multiple=True,
              help="Rule file - repeatable [.rules]")
@click.option('--datadir', type=str, metavar='DIRNAME',
              help="Data folder [.]")
@click.option('--htmldir', type=str, metavar='DIRNAME',
              help="Data folder, urlified [.html]")
@click.option('--backupdir', type=str, metavar='DIRNAME',
              help="Backup folder [.backups]")
@click.option('--backup-depth', type=int, metavar='INT',
              help="Backup depth [3]")
@click.option('--debug', type=bool, is_flag=True,
              help="Run verbosely")
@click.version_option('0.1.2', help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, config, rules, datadir, htmldir, backupdir, backup_depth, debug):
    """Rebuild plain-text todo lists using rules"""

    if debug:
        print('Printing diagnostic information.')

    # Hardwired config values (before reading optional config file)
    ctx.obj = {
        'config': '.mklistsrc',
        'rules': ['.rules', ],
        'datadir': '.',
        'htmldir': '.html',
        'backupdir': '.backups',
        'backup_depth': 3,
        'debug': False}

    if debug:
        click.echo('Hardwired config defaults:')
        for key, value in ctx.obj.items():
            print("    ", key, "=", value)

    # If command line specifies non-default config file, use it
    if config:
        using_nondefault_configfile = True
        ctx.obj['config'] = config
        if debug:
            print(f"Will use config file, {repr(ctx.obj['config'])}.")
    else:
        using_nondefault_configfile = False

    # Try to read configfile and use it to update ctx.obj
    # If configfile does not exist, write ctx.obj to a YAML file
    try:
        with open(ctx.obj['config']) as configfile:
            ctx.obj.update(yaml.load(configfile))
        if debug:
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
        if debug:
            print(f"Will use rule file(s) {repr(ctx.obj['rules'])}.")

    if datadir:
        ctx.obj['datadir'] = datadir
        if debug:
            print(f"Will use data folder {repr(ctx.obj['datadir'])}.")

    if htmldir:
        ctx.obj['htmldir'] = htmldir
        if debug:
            print(f"Will use urlified data folder {repr(ctx.obj['htmldir'])}.")

    if backupdir:
        ctx.obj['backupdir'] = backupdir
        if debug:
            print(f"Will use backups folder {repr(ctx.obj['htmldir'])}.")

    if backup_depth:
        ctx.obj['backup_depth'] = backup_depth
        if debug:
            print(f"Will keep last {repr(ctx.obj['backup_depth'])} backups.")

    if debug:
        ctx.obj['debug'] = debug
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
    print(f"* Check data folder: {repr(ctx.obj['datadir'])}.")
    print(f"* Get data: {repr(ctx.obj['datadir'])}.")
    print(f"* Apply rules to data, modifying data dictionary.")
    print(f"* Double-check for data loss??")
    print(f"* Create (or use) time-stamped folder within backup folder.")
    print(f"* Move files to time-stamped backup folder.")
    print(f"* Write out data dictionary as files in data folder.")
    print(f"* Verify that no data lost?.")
    print(f"* Move files as per ['files2dirs'].")


@cli.command()
@click.pass_context
def verify(ctx):
    """Check rules and data folder, verbosely"""

    print(f"* Get rules: {repr(ctx.obj['rules'])}, verbosely.")
    print(f"* Check data folder {repr(ctx.obj['datadir'])}, verbosely.")


class ConfigFileNotFoundError(SystemExit):
    """Specified (non-default) configuration file was not found"""
