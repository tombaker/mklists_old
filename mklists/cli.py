"""CLI - command-line interface module"""

# import os
import click


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Reorder plaintext lists by tweaking rules"""


@cli.command()
@click.option("--with-examples", is_flag=True, help="Initialize with example data")
@click.help_option(help="Show help and exit")
@click.pass_context
def init(config, with_examples):
    """Initialize list repo
    @@@TODO Add argument: optional directory name of mklists repository.
    """
    # write_config_yamlfile_to_rootdir()
    # write_minimal_rule_yamlfiles_to_somedirs()
    # if with_examples:
    #     write_example_config_yamlfile()
    #     write_example_datafiles_to_somedirs()
    #     write_example_rule_yamlfiles_to_somedirs()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--here-only", is_flag=True, help="Run only in current data directory")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun, here_only):  # should be config
    """Rebuild lists, by default in whole repo"""

    # datadir_pathname       = os.getcwd()
    # rootdir_pathname       = return_rootdir_pathname(
    #                              _datadir_pathname=datadir_pathname
    #                              _config_yamlfile_name=CONFIG_YAMLFILE_NAME)
    # ctx.obj                = return_config_dict_from_config_yamlfile(
    #                              _config_yamlfile_name=CONFIG_YAMLFILE_NAME)

    # if here_only:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _somedir_pathname=datadir_pathname,
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME)
    # else:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _somedir_pathname=rootdir_pathname,
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME)

    # for datadir in datadirs_pathnames:
    #     rulefile_pathnames_chain     = return_rulefile_pathnames_list(
    #                                    _startdir_pathname=datadir,
    #                                    _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    #                                    _config_yamlfile_name=CONFIG_YAMLFILE_NAME)
    #
    #     datadir_pathname   = os.getcwd(datadit)
    #
    #     visiblefiles_list  = return_visiblefiles_list(_datadir_pathname=datadir_pathname)
    #
    #     datalines_list     = return_datalines_list_from_datafiles(
    #                              _datafiles_names=visiblefiles_list)
    #
    #     backup_shortname   = return_backupdir_shortname(
    #                              _datadir_pathname=datadir_pathname,
    #                              _rootdir_pathname=rootdir_pathname)
    #
    #     backups_dirname    = [[get from ctx.obj <= config files]]
    #
    #     backupdir_pathname = return_backupdir_pathname(
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
    #     @@REWRITE THE FOLLOWING TO TAKE rule_yamlfile
    #     ruleobj_list       = return_ruleobj_list_from_rulefile_chain(
    #                              config_yamlfile=CONFIG_YAMLFILE_NAME, # needed??
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    #                              verbose=True)
    #
    #     datalines_dict     = return_name2lines_dict_by_applying_ruleobjs(
    #                              _ruleobjs_list=ruleobj_list,
    #                              _datalines_list=datalines_list)
    #
    #     write_datafiles_from_name2lines_dict(_name2lines_dict=None)
    #
    #     if files2dirs_dict:
    #         move_specified_datafiles_to_somedirs(ctx.obj["files2dirs_dict"])

    # Writing out HTML versions
    # if html:
    #     [create html directory]
    #     write_htmlfiles_from_name2lines_dict(lines)     - todo.py
