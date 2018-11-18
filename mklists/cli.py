"""CLI - command-line interface module"""

import glob
import click
import yaml
from mklists.apply import apply_rules_to_datalines
from mklists.readwrite import (
    get_datalines,
    get_rules,
    move_datafiles_to_backup,
    move_files_to_given_destinations,
    write_initial_rulefiles,
    write_data_dict_to_diskfiles,
    write_data_dict_urlified_to_diskfiles,
)
from mklists import MKLISTS_YAML_NAME, MKLISTS_YAML_STARTER_DICT


@click.group()
@click.option("--backups", type=int, metavar="INT", help="Keep [3] backups")
@click.option("--html", type=bool, is_flag=True, help="Make urlified copies")
@click.option("--verbose", type=bool, is_flag=True, help="Print debug info")
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, backups, html, verbose):
    """Organize your todo lists by tweaking rules"""
    overrides_from_cli = locals().copy()
    ctx.obj = MKLISTS_YAML_STARTER_DICT
    if ctx.invoked_subcommand != "init":
        overrides_from_file = _read_overrides_from_file(MKLISTS_YAML_NAME)
        ctx.obj = _apply_overrides(ctx.obj, overrides_from_file)
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
    move_datafiles_to_backup(backup_depth, verbose)
    write_data_dict_to_diskfiles(data_dict, verbose)

    if html:
        write_data_dict_urlified_to_diskfiles(data_dict, verbose)
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


@cli.command()
@click.option("--multi", type=bool, is_flag=True, help="Set up multiple dirs")
@click.pass_context
def init(ctx):
    """Write starter configuration and rule files."""
    verbose = ctx.obj["verbose"]
    _write_initial_configfile(ctx.obj)
    write_initial_rulefiles()


def _write_initial_configfile(settings_dict=None):
    """Writes initial configuration file to disk."""
    if os.path.exists(MKLISTS_YAML_NAME):
        raise InitError(f"{repr(MKLISTS_YAML_NAME)} already initialized.")
    else:
        print(f"Writing starter config file {repr(MKLISTS_YAML_NAME)}.")
        with open(configfile_name, "w") as fout:
            fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
