"""CLI - command-line interface module"""

import glob
import click
import yaml
from mklists.rules import apply_rules_to_datalines
from mklists.cli_init import (
    get_rules,
    write_initial_configfile,
    write_initial_rulefiles,
)
from mklists.cli_run import (
    get_datalines,
    move_datafiles_to_backup,
    move_files_between_folders,
    write_data_to_files,
    write_data_urlified_to_files,
)
from mklists.verbose import explain
from mklists import (
    MKLISTSRC_LOCAL_NAME,
    LOCAL_RULEFILE_NAME,
    MKLISTSRC_STARTER_DICT,
)


@click.group()
@click.option(
    "--backup-depth",
    type=int,
    metavar="INT",
    help="Rolling backups to keep [default: '3']",
)
@click.option(
    "--urlify",
    type=bool,
    is_flag=True,
    help="Copy data to clickable-link HTML",
)
@click.option("--verbose", type=bool, is_flag=True, help="Enable verbose mode")
@click.version_option("0.1.4", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx, backup_depth, urlify, verbose):
    """Sync your plain-text todo lists to evolving rules"""

    overrides_from_cli = locals().copy()
    ctx.obj = MKLISTSRC_STARTER_DICT
    if ctx.invoked_subcommand != "init":
        overrides_from_file = read_overrides_from_file(MKLISTSRC_NAME)
        ctx.obj = apply_overrides(ctx.obj, overrides_from_file)

    # Override settings in context object from snapshot of CLI arguments.
    ctx.obj = apply_overrides(ctx.obj, overrides_from_cli)

    # Explain settings in context object.
    if verbose:
        explain(**ctx.obj)


@cli.command()
@click.option(
    "--repo",
    type=bool,
    is_flag=True,
    help="Initialize as multi-list-folder repo",
)
@click.pass_context
def init(ctx, repo):
    """Generate default configuration and rule files."""

    verbose_bool = ctx.obj["verbose"]
    write_initial_configfile(settings_dict=ctx.obj, verbose=verbose_bool)
    write_initial_rulefiles(verbose=verbose_bool)


@cli.command()
@click.pass_context
def run(ctx):
    """Read and apply rules to re-write data files"""
    # Read rule files and return aggregated list of rules objects.
    rules = get_rules(
        global_rulefile_name=ctx.obj["globalrules"],
        local_rulefile_name=ctx.obj["rules"],
        valid_filename_chars=ctx.obj["valid_filename_chars"],
        verbose=ctx.obj["verbose"],
    )

    # Read files in working directory and return aggregated list of lines.
    datalines = get_datalines(
        ls_visible=[name for name in glob.glob("*")],
        but_not=ctx.obj["invalid_filename_patterns"],
        verbose=ctx.obj["verbose"],
    )

    # Apply rules (keys) to datalines (values) within a dictionary.
    mklists_dict = apply_rules_to_datalines(
        ruleobjs_list=rules, datalines_list=datalines
    )

    # If 'backup' is ON:
    # before writing mklists_dict contents to disk,
    # creates timestamped backup directory in specified backup_dir,
    # and moves all visible files in data directory to backup directory.
    if ctx.obj["backup"]:
        move_datafiles_to_backup(
            ls_visible=[name for name in glob.glob("*")],
            backup=True,  # 2018-09-02: just for now?
            backup_dir=ctx.obj["backup_dir"],
            backup_depth=ctx.obj["backup_depth"],
        )

    # If 'backup' is ON, move existing files from working to backup directory.
    # If 'backup' is OFF, DELETE existing files in working directory.
    # Write mklists_dict to working directory:
    # -- mklists_dict keys are names of files.
    # -- mklists_dict values are contents of files.
    write_data_to_files(datalines_d=mklists_dict, verbose=ctx.obj["verbose"])

    # If 'urlify' is ON, write urlified data files to urlify_dir.
    if ctx.obj["urlify"]:
        write_data_urlified_to_files(
            datalines_d=mklists_dict,
            urlify_dir=ctx.obj["urlify_dir"],
            urlify_depth=ctx.obj["urlify_depth"],
            verbose=ctx.obj["verbose"],
        )

    # If 'files2dirs' is ON, move selected files to external directories.
    if ctx.obj["files2dirs"]:
        move_files_to_external_directories(ctx.obj["files2dirs"])


def read_overrides_from_file(configfile_name):
    """docstring"""
    return yaml.load(open(configfile_name).read())


def apply_overrides(settings_dict, overrides):
    """docstring"""
    overrides.pop("ctx", None)
    overrides = {
        key: overrides[key] for key in overrides if overrides[key] is not None
    }
    settings_dict.update(overrides)
    return settings_dict
