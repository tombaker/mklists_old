"""CLI - command-line interface module"""

import click
import yaml
from mklists import CONFIG_STARTER_DICT, CONFIGFILE_NAME
from mklists.apply import apply_rules_to_datalines
from mklists.readwrite import (
    move_old_datafiles_to_backupdirs,
    write_dataobj_to_textfiles,
    write_dataobj_to_htmlfiles,
    move_certain_datafiles_to_other_directories,
    get_rules_from_localrulefile,
    get_rules_from_rulefile,
    get_rules_from_globalconfigfile,
)
from mklists.utils import update_settings_dict, get_list_of_lines_from_all_datafiles


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
    another_snapshot_of_commandline_options = locals().copy()
    print(another_snapshot_of_commandline_options)
    if ctx:
        print(repr(ctx))
    if empty is not None:
        print("empty")
    elif newbie is not None:
        print("newbie")
        print("call write_initial_configfile() - in readwrite.py")
        print("call write_initial_rulefiles() - in readwrite.py")


@cli.command()
@click.option("--dryrun", is_flag=True, help="Read-only, verbosely")
@click.pass_context
def run(ctx, dryrun):
    """Apply rules to re-write data files.
    @@@for dir in .rules..."""
    localrules = get_rules_from_localrulefile()
    rules = get_rules_from_rulefile()
    globalrules = get_rules_from_globalconfigfile()
    data = get_list_of_lines_from_all_datafiles()
    all_datalines_dict = apply_rules_to_datalines(globalrules, localrules, rules, data)
    move_old_datafiles_to_backupdirs(ctx)
    write_dataobj_to_textfiles(all_datalines_dict)
    if ctx.obj["html"]:
        write_dataobj_to_htmlfiles(all_datalines_dict)
    if ctx.obj["files2dirs"]:
        move_certain_datafiles_to_other_directories(ctx.obj["files2dirs"])
    if dryrun:
        print("chose dryrun")


@cli.command()
@click.pass_context
def testme(ctx):
    """Subcommand for various tests."""
    from mklists.utils import find_project_root

    print(ctx.params)
    find_project_root()
