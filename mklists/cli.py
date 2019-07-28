"""CLI - command-line interface module"""

import click


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Rebuild your todo lists by tweaking rules"""


@cli.command()
@click.option("--newbie", is_flag=True, help="Initialize with example data and config")
@click.help_option(help="Show help and exit")
@click.pass_context
def init(ctx, newbie):
    """Initialize list repo"""
    import os

    print(os.getcwd())
    # write_initial_config_yamlfile()
    # write_initial_rule_yamlfiles()
    # if newbie:
    #     write_example_rule_yamlfiles()
    #     write_example_datafiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--here", is_flag=True, help="Run in current working directory only")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun, here):
    """Rebuild lists in (by default) entire repo"""
    # ctx.obj    = load_config_yamlfile()
    # lines_list = return_datalines_list_from_datafiles(datafiles)
    #              use utils.py: return_visiblefiles_list() - ?
    # rules_objs = return_ruleobj_list_from_rule_yamlfiles()
    #
    # return_datalines_dict_after_applying_rules(rule_objs, lines_list)
    # move_datafiles_to_backupdir(ctx?)            - todo.py
    # write_datafiles_from_datadict(lines)      - todo.py
    #
    # Next -----
    # return_backupdir_pathname, then os.mkdir(backupdir)     - utils.py
    # Get number of backups as configuring (config['backups']
    #     If backups less than two, then backups = 2 ("mandatory")
    # Create a backup directory.
    #     Generate a name for backupdir (return_backupdir_pathname).
    #     Make dir: hard-coded parent dirname (.backups) plus generated timestamped name.
    # delete_older_backups()                            - todo.py
    #
    # Then -----
    # if html:
    #     write_datadict_to_htmlfiles_in_htmldir(lines)     - todo.py
    # if files2dirs:
    #     move_certain_datafiles_to_other_directories(ctx.obj["files2dirs"])
