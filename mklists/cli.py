"""CLI - command-line interface module"""

import glob
import click
import yaml
from mklists.apply import apply_rules_to_datalines
from mklists.cli_init import (
    get_rules,
    write_initial_configfile,
    write_initial_rulefiles,
)
from mklists.cli_run import (
    get_datalines,
    move_datafiles_to_backup,
    move_files_to_given_destinations,
    write_mklists_dict_to_diskfiles,
    write_mklists_dict_urlified_to_file,
)
from mklists import (
    MKLISTSRC_LOCAL_NAME,
    RULEFILE_NAME,
    LOCAL_RULEFILE_NAME,
    MKLISTSRC_STARTER_DICT,
)


@click.group()
@click.option("--backups", type=int, metavar="INT", help="Enable [3] backups")
@click.option("--html", type=bool, is_flag=True, help="Enable urlified copies")
@click.option("--verbose", type=bool, is_flag=True, help="Enable verbose mode")
@click.version_option("0.1.4", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, backups, html, verbose):
    """Organize your todo lists by tweaking rules"""

    overrides_from_cli = locals().copy()
    ctx.obj = MKLISTSRC_STARTER_DICT
    if ctx.invoked_subcommand != "init":
        overrides_from_file = _read_overrides_from_file(MKLISTSRC_NAME)
        ctx.obj = _apply_overrides(ctx.obj, overrides_from_file)

    ctx.obj = _apply_overrides(ctx.obj, overrides_from_cli)


@cli.command()
@click.option(
    "--repo", type=bool, is_flag=True, help="Initialize as multi-folder repo"
)
@click.pass_context
def init(ctx, repo):
    """Initialize folder with config and rule files"""

    verbose = ctx.obj["verbose"]
    write_initial_configfile(ctx.obj, verbose)
    write_initial_rulefiles(verbose)


@cli.command()
@click.pass_context
def run(ctx):
    """Apply rules to re-write data files"""

    good_chars = ctx.obj["valid_filename_chars"]
    bad_patterns = ctx.obj["invalid_filename_patterns"]
    verbose = ctx.obj["verbose"]
    html = ctx.obj["html"]
    if backups:
        backup_depth = ctx.obj["backup_depth"]
    if ctx.obj["files2dirs"]:
        files2dirs = ctx.obj["files2dirs"]

    ruleobj_list = get_rules(good_chars, bad_patterns, verbose)
    datalines_list = get_datalines(good_chars, bad_patterns, verbose)
    mklists_dict = apply_rules_to_datalines(ruleobj_list, datalines_list)

    if backups:
        move_datafiles_to_backup(backup_depth)
    else:
        delete_datafiles()

    write_mklists_dict_to_diskfiles(mklists_dict, verbose)

    if html:
        write_mklists_dict_urlified_to_file(mklists_dict, verbose)

    if files2dirs:
        move_files_to_given_destinations(files2dirs)


def _read_overrides_from_file(configfile_name):
    """docstring"""
    return yaml.load(open(configfile_name).read())


def _apply_overrides(settings_dict, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {
        key: overrides[key] for key in overrides if overrides[key] is not None
    }
    settings_dict.update(overrides)
    return settings_dict
