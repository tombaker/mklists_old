"""CLI - command-line interface module"""

import click

# from .run import (
#    apply_rules_to_datalines,
#    load_datalines_from_listfiles,
#    load_rules_from_rule_yamlfiles,
#    move_certain_listfiles_to_other_directories,
#    move_existing_listfiles_to_backupdir,
#    write_datadict_to_htmlfiles_in_htmldir,
#    write_datadict_to_listfiles_in_currentdir,
# )
# from .todo import (
#    delete_older_backups,
#    get_ctxobj_from_config_yamlfile,
#    move_certain_listfiles_to_other_directories,
#    move_existing_listfiles_to_backupdir,
#    write_datadict_to_htmlfiles_in_htmldir,
#    write_initial_rule_yamlfiles,
# )


@click.group()
@click.version_option("0.1.5", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(ctx):
    """Sync list files to your evolving rules"""


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def init(ctx):
    """Initialize list repo"""
    # write_initial_config_yamlfile()
    # write_initial_rule_yamlfiles()


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def newbie(ctx):
    """Initialize list repo with example files"""
    # write_initial_config_yamlfile()
    # write_example_rule_yamlfiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.option("--quiet", is_flag=True, help="Run silently, errors excepted")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun, quiet):
    """Sync list files to rules"""
    # ctx.obj    = load_config_yamlfile()
    # lines_list = load_datalines_from_listfiles(listfiles)
    #              use utils.py: ls_visible() - ?
    # rules_objs = load_rules_from_rule_yamlfiles()
    #
    # apply_rules_to_datalines(rule_objs, lines_list)
    # move_existing_listfiles_to_backupdir(ctx?)            - todo.py
    # write_datadict_to_listfiles_in_currentdir(lines)      - todo.py
    #
    # STAGE1     make_backupdir_name, then os.mkdir(backupdir)     - utils.py
    # STAGE1     delete_older_backups()                            - todo.py
    #
    # STAGE2 if html:
    # STAGE2     write_datadict_to_htmlfiles_in_htmldir(lines)     - todo.py
    # STAGE2 if files2dirs:
    # STAGE2     move_certain_listfiles_to_other_directories(ctx.obj["files2dirs"])
