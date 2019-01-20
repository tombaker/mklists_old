"""CLI - command-line interface module"""

import click
from .makelists_todo import (
    get_ruleobj_list_from_rule_yamlfiles,
    move_existing_listfiles_to_backupdir,
    move_certain_listfiles_to_other_directories,
)

# from makelists_todo.py:
#    move_existing_listfiles_to_backupdir,
#    write_datadict_to_listfiles,
#    write_datadict_to_htmlfiles,
#    move_certain_listfiles_to_other_directories,
from .makelists import get_dataline_list_from_listfiles, apply_rules_to_datalines


@click.group()
@click.version_option("0.1.5", help="Show version and exit.")
@click.help_option(help="Show help and exit.")
@click.pass_context
def cli(ctx):
    """Organize your todo lists by tweaking rules"""


@cli.command()
@click.option("--empty", is_flag=True, help="Minimal configuration (for experts).")
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
    """Apply rules to re-write data files."""
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
