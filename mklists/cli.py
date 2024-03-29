"""CLI - command-line interface module"""

# import os
# from pathlib import Path
import click


# pylint: disable=unused-argument
#         During development, unused arguments here.
# pylint: disable=unexpected-keyword-arg
#         Pylint does not like click parameter "required"


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(config):
    """Sync your lists to evolving rules."""


@cli.command()
@click.argument("directory", click.Path(exists=False, required=False))
@click.help_option(help="Show help and exit")
@click.pass_context
def init(config, directory):
    """Initialize list repo."""
    # if directory:
    #     dir = Path.cwd().joinpath(directory)
    #     os.chdir(dir)
    # write_starter_configfile()
    # write_starter_rulefiles()


@cli.command()
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--here-only", is_flag=True, help="Run only in current data directory")
@click.help_option(help="Show help and exit")
@click.pass_context
def sync(config, dryrun, here_only):  # should be config
    """Rebuild lists, by default in whole repo"""

    # ctx.obj                = read_configfile()

    # if here_only: # will operate only on data directories below current directory
    #     datadir_pathnames  = get_datadir_paths(
    # else: # will operate on all data directories under repo rootdir
    #     datadir_pathnames  = return_data_subdirs_list(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _somedir_pathname=rootdir_pathname,
    #                              _rules_csvfile_name=RULE_CSVFILE_NAME)

    # for datadir in datadirs_pathnames:
    #     rulefile_pathnames_chain     = _return_rulefile_chain(
    #                                    _startdir_pathname=datadir,
    #                                    _rules_csvfile_name=RULE_CSVFILE_NAME,
    #                                    _configfile_name=CONFIGFILE_NAME)
    #
    #     visiblefiles_list  = get_visible_filenames()
    #
    #     datalines_list     = read_datafiles()
    #
    #     backup_shortname   = return_backupdir_shortname(
    #                              _datadir_pathname=datadir_pathname,
    #                              _rootdir_pathname=rootdir_pathname)
    #
    #     backups_dirname    = [[get from ctx.obj <= config files]]
    #
    #     backupdir_pathname = get_backupdir_path(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _backupdir_subdir_name=backups_dirname,
    #                              _backupdir_shortname=backup_shortname,
    #                              _timestamp_str=TIMESTAMP_STR)
    #
    #     move_all_datafiles_to_backupdir(
    #         _datadir_pathname=datadir_pathname,
    #         _datafiles_names=visiblefiles_list,
    #         _backupdir_pathname=backupdir_pathname)
    #
    #     delete_older_backupdirs(
    #         _rootdir_pathname=None,
    #         _backupdir_pathname=None,
    #         _backupdir_shortname=None,
    #         _backup_depth_int=None)            # something like config['backups']
    #
    #
    #     @@REWRITE THE FOLLOWING TO TAKE rules_csvfile
    #     ruleobj_list       = return_ruleobj_list_from_rulefile_chain(
    #                              configfile=CONFIGFILE_NAME, # needed??
    #                              _rules_csvfile_name=RULE_CSVFILE_NAME,
    #                              verbose=True)
    #
    #     datalines_dict     = apply_rules_to_datalines(
    #                              _ruleobjs_list=ruleobj_list,
    #                              _datalines_list=datalines_list)
    #
    #     write_new_datafiles(_name2lines_dict=None)
    #
    #     if files2dirs_dict:
    #         move_specified_datafiles_elsewhere(ctx.obj["files2dirs_dict"])
    # Writing out HTML versions
    # if html:
    #     [create html directory]
    #     write_htmlfiles_from_name2lines_dict(lines)     - todo.py
