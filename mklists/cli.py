"""CLI - command-line interface module"""

import glob
import click
import os
import yaml
from mklists.apply import apply_rules_to_datalines
from mklists.readwrite import (
    get_datalines,
    move_old_datafiles_to_backup,
    move_certain_datafiles_to_other_directories,
    write_data_dict_object_to_diskfiles,
    write_data_dict_urlified_to_diskfiles,
)
from mklists import (
    LOCAL_RULEFILE_NAME,
    RULEFILE_NAME,
    RULEFILE_STARTER_YAMLSTR,
    CONFIGFILE_NAME,
    CONFIG_STARTER_DICT,
)
from mklists.rules import get_rules


@click.group()
@click.option("--html", type=bool, is_flag=True, help="Make urlified copies")
@click.option("--verbose", type=bool, is_flag=True, help="Print debug info")
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, html, verbose):
    """Organize your todo lists by tweaking rules"""
    overrides_from_cli = locals().copy()
    ctx.obj = CONFIG_STARTER_DICT
    # if ctx.invoked_subcommand != "init":
    #    overrides_from_file = _read_overrides_from_file(CONFIGFILE_NAME)
    #    ctx.obj = _apply_overrides(ctx.obj, overrides_from_file)
    ctx.obj = _apply_overrides(ctx.obj, overrides_from_cli)


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files."""
    good_chars = ctx.obj["valid_filename_chars"]
    bad_pats = ctx.obj["invalid_filename_patterns"]
    verbose = ctx.obj["verbose"]
    html = ctx.obj["html"]
    backup_depth = ctx.obj["backup_depth"] if ctx.obj["backup_depth"] else 0
    files2dirs = ctx.obj["files2dirs"] if ctx.obj["files2dirs"] else None
    ruleobj_list = get_rules()
    datalines_list = get_datalines()
    data_dict = apply_rules_to_datalines(ruleobj_list, datalines_list)
    move_old_datafiles_to_backup(backup_depth, verbose)
    write_data_dict_object_to_diskfiles(data_dict, verbose)

    if html:
        write_data_dict_urlified_to_diskfiles(data_dict, verbose)
    if files2dirs:
        move_certain_datafiles_to_other_directories(files2dirs)


def _read_overrides_from_file(configfile_name):
    """docstring"""
    return yaml.load(open(configfile_name).read())


def _apply_overrides(settings_dict, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {key: overrides[key] for key in overrides if overrides[key] is not None}
    settings_dict.update(overrides)
    return settings_dict


@cli.command()
@click.option("--empty", type=bool, is_flag=True, help="With bare minimum")
@click.option("--newbie", type=bool, is_flag=True, help="With examples")
@click.pass_context
def init(ctx, empty, newbie):
    """Write starter configuration and rule files."""
    if empty is not None:
        print("empty")
    elif newbie is not None:
        print("newbie")


# This should work!
#    try:
#        with open(CONFIGFILE_NAME, "x") as fout:
#            fout.write(CONFIGFILE_YAMLSTR)
#            print(f"Created config file: {repr(CONFIGFILE_NAME)}.")
#    except FileExistsError:
#        raise InitError(f"{repr(CONFIGFILE_NAME)} already initialized.")


# def _write_initial_rulefiles():
#     """Writes starter files to disk: '.globalrules' and '.rules'."""
#     for directory_name, file_name, content in [
#         (LOCAL_DIR, LOCAL_RULEFILE_NAME, LOCAL_RULEFILE_STARTER_YAMLSTR)
#     ]:
#         rulefile = os.path.join(directory_name, file_name)
#         try:
#             os.makedirs(directory_name)
#             with open(rulefile, "x") as fout:
#                 fout.write(content)
#             print(f"Created starter rule file: {repr(rulefile)}.")
#         except FileExistsError:
#             print(f"Found {repr(rulefile)} - leaving untouched.")


@cli.command()
@click.pass_context
def testme(ctx):
    """Subcommand for various tests."""
    from mklists.utils import get_rootdir

    get_rootdir()
