"""CLI - command-line interface module"""

import click
from mklists.apply import apply_rules_to_datalines
from mklists.readwrite import (
    read_settings_from_configfile,
    update_settings,
    get_datalines,
    move_old_datafiles_to_backupdirs,
    write_dataobj_to_textfiles,
    write_dataobj_to_htmlfiles,
    move_certain_datafiles_to_other_directories,
)
from mklists import CONFIG_STARTER_DICT, CONFIGFILE_NAME
from mklists.rules import get_rules


@click.group()
@click.option("--verbose", type=bool, is_flag=True, help="Print debug info")
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, verbose):
    """Organize your todo lists by tweaking rules"""
    snapshot_of_cli_options = locals().copy()
    ctx.obj = CONFIG_STARTER_DICT
    if verbose:
        print(f"Reading minimal configuration: {CONFIG_STARTER_DICT}")
    if ctx.invoked_subcommand != "init":
        config_settings_from_file = read_settings_from_configfile(CONFIGFILE_NAME)
        ctx.obj = update_settings(ctx.obj, config_settings_from_file)
    ctx.obj = update_settings(ctx.obj, snapshot_of_cli_options)


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files.
    @@@for dir in .rules..."""
    ruleobj_list = get_rules()
    dataobj_list = get_datalines()
    dataobj_dict = apply_rules_to_datalines(ruleobj_list, dataobj_list)
    move_old_datafiles_to_backupdirs(ctx)
    write_dataobj_to_textfiles(dataobj_dict)
    if ctx.obj["html"]:
        write_dataobj_to_htmlfiles(dataobj_dict)
    if ctx.obj["files2dirs"]:
        move_certain_datafiles_to_other_directories(ctx.obj["files2dirs"])


@cli.command()
@click.option("--empty", type=bool, is_flag=True, help="With bare minimum")
@click.option("--newbie", type=bool, is_flag=True, help="With examples")
@click.pass_context
def init(ctx, empty, newbie):
    """Write starter configuration and rule files."""
    if ctx:
        print(repr(ctx))
    if empty is not None:
        print("empty")
    elif newbie is not None:
        print("newbie")
        print("call write_initial_configfile() - in readwrite.py")
        print("call write_initial_rulefiles() - in readwrite.py")


@cli.command()
@click.pass_context
def testme(ctx):
    """Subcommand for various tests."""
    from mklists.utils import find_project_root

    print(ctx.params)
    find_project_root()
