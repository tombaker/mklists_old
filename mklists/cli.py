"""CLI - command-line interface module"""

import click
import yaml
from mklists import CONFIG_STARTER_DICT, CONFIGFILE_NAME
from mklists.todo import (
    get_ruleobjs_list_from_files,
    move_old_listfiles_to_backupdir,
    move_certain_listfiles_to_other_directories,
)
from mklists.makelists import (
    get_datalines_from_listfiles,
    apply_rules_to_datalines,
    write_pydict_to_listfiles,
    write_pydict_to_htmlfiles,
)
from mklists.utils import get_rootdir_name, update_settings_dict


@click.group()
@click.option("--verbose", is_flag=True, help="Print debug info")
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, verbose):
    """Organize your todo lists by tweaking rules"""
    snapshot_of_commandline_options = locals().copy()
    snapshot_of_commandline_options.pop("ctx", None)
    ctx.obj = CONFIG_STARTER_DICT
    if verbose:
        print(f"Reading minimal configuration: {CONFIG_STARTER_DICT}")
    if ctx.invoked_subcommand != "init":
        settings_from_configfile = yaml.load(open(CONFIGFILE_NAME).read())
        ctx.obj = update_settings_dict(ctx.obj, settings_from_configfile)
    ctx.obj = update_settings_dict(ctx.obj, snapshot_of_commandline_options)


@cli.command()
@click.option("--empty", is_flag=True, help="With bare minimum")
@click.option("--newbie", is_flag=True, help="With examples")
@click.pass_context
def init(ctx, empty, newbie):
    """Write starter configuration and rule files."""
    if empty is not None:
        print("empty")
    elif newbie is not None:
        print("newbie")
        print("call write_initial_configfile() - in writes.py")
        print("call write_initial_rulefiles() - in writes.py")


@cli.command()
@click.option("--dryrun", is_flag=True, help="Read-only, verbosely")
@click.pass_context
def run(ctx, dryrun):
    """Apply rules to re-write data files.
    @@@for dir in .rules..."""
    data = get_datalines_from_listfiles()
    rules = get_ruleobjs_list_from_files()
    all_datalines_dict = apply_rules_to_datalines(rules, data)
    move_old_listfiles_to_backupdir(ctx)
    write_pydict_to_listfiles(all_datalines_dict)
    if ctx.obj["html"]:
        write_pydict_to_htmlfiles(all_datalines_dict)
    if ctx.obj["files2dirs"]:
        move_certain_listfiles_to_other_directories(ctx.obj["files2dirs"])
    if dryrun:
        print("chose dryrun")


@cli.command()
@click.pass_context
def testme(ctx):
    """Subcommand for various tests."""
    print(ctx.params)
    name = get_rootdir_name()
    print(name)
