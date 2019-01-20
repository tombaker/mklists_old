"""CLI - command-line interface module"""

import click
import yaml
from mklists import CONFIG_STARTER_DICT, CONFIG_YAMLFILE_NAME
from .todo import (
    get_ruleobj_list_from_rule_yamlfiles,
    move_existing_listfiles_to_backupdir,
    move_certain_listfiles_to_other_directories,
)

# Will be in makelists.py:
#    move_existing_listfiles_to_backupdir,
#    write_datadict_to_listfiles,
#    write_datadict_to_htmlfiles,
#    move_certain_listfiles_to_other_directories,
from .makelists import get_dataline_list_from_listfiles, apply_rules_to_datalines
from .utils import get_rootdir_name, update_settings_dict


@click.group()
@click.option("--verbose", is_flag=True, help="Print debug information.")
@click.version_option("0.1.5", help="Show version and exit.")
@click.help_option(help="Show help and exit.")
@click.pass_context
def cli(ctx, verbose):
    """Organize your todo lists by tweaking rules"""
    snapshot_of_commandline_options = locals().copy()
    snapshot_of_commandline_options.pop("ctx", None)
    ctx.obj = CONFIG_STARTER_DICT
    if verbose:
        print(f"Reading minimal configuration: {CONFIG_STARTER_DICT}")
    if ctx.invoked_subcommand != "init":
        settings_from_config_yamlfile = yaml.load(open(CONFIG_YAMLFILE_NAME).read())
        ctx.obj = update_settings_dict(ctx.obj, settings_from_config_yamlfile)
    ctx.obj = update_settings_dict(ctx.obj, snapshot_of_commandline_options)


@cli.command()
@click.option(
    "--empty", is_flag=True, help="Write bare minimum configuration (for experts)."
)
@click.pass_context
def init(ctx, empty):
    """Write starter configuration and rule files."""
    if empty:
        print("empty")

    # write_initial_config_yamlfile() - in writes.py
    # write_initial_rule_yamlfiles() - in writes.py


@cli.command()
@click.option("--dryrun", is_flag=True, help="Read-only, verbosely")
@click.pass_context
def run(ctx, dryrun):
    """Apply rules to re-write data files.
    @@@for dir in .rules..."""
    data = get_dataline_list_from_listfiles()
    rules = get_ruleobj_list_from_rule_yamlfiles()
    all_datalines_dict = apply_rules_to_datalines(rules, data)
    print(all_datalines_dict.keys())
    move_existing_listfiles_to_backupdir(ctx)
    # write_datadict_to_listfiles(all_datalines_dict)
    if ctx.obj["html"]:
        # write_datadict_to_htmlfiles(all_datalines_dict)
        pass
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
