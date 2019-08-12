"""CLI - command-line interface module"""

# import os
import click


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Recompose plain text lists by tweaking rules"""


@cli.command()
@click.option("--newbie", is_flag=True, help="Initialize with example data and config")
@click.help_option(help="Show help and exit")
@click.pass_context
def init(config, newbie):
    """Initialize list repo"""
    # write_minimal_config_yamlfile()
    # write_minimal_rule_yamlfiles()
    # if newbie:
    #     write_newbie_config_yamlfile()
    #     write_newbie_datafiles()
    #     write_newbie_rule_yamlfiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--here-only", is_flag=True, help="Run only in current data directory")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun, here_only):  # should be config
    """Rebuild lists, by default in whole repo"""

    # currentdir_pathname    = os.getcwd()
    # rootdir_pathname       = return_rootdir_pathname(
    #                              _currentdir_pathname=currentdir_pathname
    #                              _config_yamlfile_name=CONFIG_YAMLFILE_NAME)
    # ctx.obj               = return_pyobj_from_yamlfile(
    #                              _generic_yamlfile_name=CONFIG_YAMLFILE_NAME)

    # if here_only:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _somedir_pathname=currentdir_pathname,
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME)
    # else:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              _rootdir_pathname=rootdir_pathname,
    #                              _somedir_pathname=rootdir_pathname,
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME)

    # for datadir in datadirs_pathnames:
    #     rulefile_pathnames_chain     = return_rulefile_pathnames_chain_as_list(
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
    #                              _backupdir_pathname=backups_dirname,
    #                              _backupdir_shortname=backup_shortname,
    #                              _timestamp_str=TIMESTAMP_STR)
    #
    #     move_datafiles_to_backupdir(
    #         _datadir_pathname=datadir_pathname,
    #         _datafiles_names=visiblefiles_list,
    #         _backupdir_pathname=backupdir_pathname)
    #
    #     delete_older_backups(
    #         _rootdir_pathname=None,
    #         _backupdir_pathname=None,
    #         _backupdir_shortname=None,
    #         _backup_depth_int=None)            # something like config['backups']
    #
    #
    #     @@REWRITE THE FOLLOWING TO TAKE rulefile_pathnames_chain
    #     ruleobj_list       = return_ruleobj_list_from_rule_yamlfiles(
    #                              config_yamlfile=CONFIG_YAMLFILE_NAME, # needed??
    #                              _rule_yamlfile_name=RULE_YAMLFILE_NAME,
    #                              verbose=True)
    #                              Shouldn't this be a chain of rule files?
    #
    #     datalines_dict     = return_filename2datalines_dict_after_applying_rules(
    #                              _ruleobjs_list=ruleobj_list,
    #                              _datalines_list=datalines_list)
    #
    #     write_datafiles_from_datadict(_filename2datalines_dict=None)
    #
    #     if files2dirs_dict:
    #         relocate_specified_datafiles_elsewhere(ctx.obj["files2dirs_dict"])

    # Writing out HTML versions
    # if html:
    #     [create html directory]
    #     write_htmlfiles_from_datadict(lines)     - todo.py
