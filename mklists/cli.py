"""CLI - command-line interface module"""

import click
import os


class Config:
    """Factory for configuration object."""


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Rebuild your todo lists by tweaking rules"""
    config = ctx.obj = Config()
    config.foo = 1


@cli.command()
@click.option("--newbie", is_flag=True, help="Initialize with example data and config")
@click.help_option(help="Show help and exit")
@pass_config
def init(config, newbie):
    """Initialize list repo"""
    print("init ------")
    print(type(config))
    print(config.foo)
    # write_initial_config_yamlfile()
    # write_initial_rule_yamlfiles()
    # if newbie:
    #     write_newbie_rule_yamlfiles()
    #     write_newbie_datafiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--all", is_flag=True, help="Run in all data directories")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun, all):  # should be config
    """Rebuild lists in (by default) entire repo"""

    # rootdir_pathname   = return_rootdir_pathname(
    #                          cwd=os.getcwd()
    #                          configfile_name=CONFIG_YAMLFILE_NAME)
    #
    # ctx.obj            = load_config_yamlfile(mklists_config_yamlfile=CONFIG_YAMLFILE_NAME)

    # if all:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              somedir_pathname=rootdir_pathname,
    #                              rulefile_name=RULE_YAMLFILE_NAME)
    # else:
    #     datadir_pathnames  = return_datadir_pathnames_under_somedir(
    #                              somedir_pathname=os.getcwd(),
    #                              rulefile_name=RULE_YAMLFILE_NAME)
    #     Or: datadir_pathnames = [ os.getcwd() ]

    # for datadir in datadirs_pathnames:
    #     datadir_pathname   = os.getcwd(datadit)
    #
    #     visiblefiles_list  = return_visiblefiles_list(datadir_name=datadir_pathname)
    #
    #     datalines_list     = return_datalines_list_from_datafiles(
    #                              datafile_names=visiblefiles_list)
    #
    #     backup_shortname   = return_backupdir_shortname(
    #                              datadir_pathname=datadir_pathname,
    #                              rootdir_pathname=rootdir_pathname)
    #
    #     backups_dirname    = [[get from ctx.obj <= config files]]
    #
    #     backupdir_pathname = return_backupdir_pathname(
    #                              rootdir_pathname=rootdir_pathname,
    #                              backups_dirname=backups_dirname,
    #                              backup_shortname=backup_shortname,
    #                              timestamp_name=TIMESTAMP_STR)
    #
    #     move_datafiles_to_backupdir(
    #         datadir_pathname=datadir_pathname,
    #         datadir_filenames=visiblefiles_list,
    #         backupdir_pathname=backupdir_pathname)
    #
    #     delete_older_backups(
    #         rootdir_pathname=None,
    #         backups_dirname=None,
    #         backup_shortname=None,
    #         backup_depth=None)            # something like config['backups']
    #
    #     rule_filenames_chain     = return_rule_filenames_chain_as_list(
    #                              start_pathname=None,
    #                              rulefile_name=RULE_YAMLFILE_NAME,
    #                              configfile_name=CONFIG_YAMLFILE_NAME)
    #
    #
    #     @@REWRITE THE FOLLOWING TO TAKE rule_filenames_chain
    #     ruleobj_list       = return_ruleobj_list_from_rule_yamlfiles(
    #                              config_yamlfile=CONFIG_YAMLFILE_NAME,   # why is this needed??
    #                              rule_yamlfile=RULE_YAMLFILE_NAME,       # shouldn't this be a chain of rule files?
    #                              verbose=True)
    #
    #     datalines_dict     = return_datalines_dict_by_applying_rules(
    #                              ruleobj_list=ruleobj_list,
    #                              dataline_list=datalines_list)
    #
    #     write_datafiles_from_datadict(datadict=None)
    #
    #     if files2dirs:
    #         relocate_specified_datafiles_elsewhere(ctx.obj["files2dirs"])

    # Writing out HTML versions
    # if html:
    #     [create html directory]
    #     write_htmlfiles_from_datadict(lines)     - todo.py
