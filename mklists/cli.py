"""CLI - command-line interface module"""

import click


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Sync list files to your evolving rules"""


@cli.command()
@click.option("--newbie", is_flag=True, help="Initialize with example data and config")
@click.help_option(help="Show help and exit")
@click.pass_context
def init(ctx, newbie):
    """Initialize list repo"""
    import os

    print(os.getcwd())
    # write_initial_config_yamlfile()
    # write_initial_rule_yamlfiles()
    # if newbie:
    #     write_example_rule_yamlfiles()
    #     write_example_datafiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun):
    """Sync list files to rules"""
    # ctx.obj    = load_config_yamlfile()
    # lines_list = load_datalines_from_datafiles(datafiles)
    #              use utils.py: ls_visible() - ?
    # rules_objs = load_rules_from_rule_yamlfiles()
    #
    # apply_rules_to_datalines(rule_objs, lines_list)
    # move_current_datafiles_to_backupdir(ctx?)            - todo.py
    # write_datadict_to_datafiles_in_currentdir(lines)      - todo.py
    #
    # Next -----
    # make_backup_dirname, then os.mkdir(backupdir)     - utils.py
    # delete_older_backups()                            - todo.py
    #
    # Then -----
    # if html:
    #     write_datadict_to_htmlfiles_in_htmldir(lines)     - todo.py
    # if files2dirs:
    #     move_certain_datafiles_to_other_directories(ctx.obj["files2dirs"])
