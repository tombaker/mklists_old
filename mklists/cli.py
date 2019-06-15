"""CLI - command-line interface module"""

import click

# from .run import (
#    apply_rules_to_datalines,
#    get_dataline_list_from_listfiles,
#    get_ruleobj_list_from_rule_yamlfiles,
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
    # initialize.py: initialize_config_yamlfiles()
    # todo.py:       write_initial_rule_yamlfiles()


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def newbie(ctx):
    """Initialize list repo with example files"""
    # initialize.py: initialize_config_yamlfiles()
    # todo.py:       write_initial_rule_yamlfiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode")
@click.help_option(help="Show help and exit")
@click.pass_context
def run(ctx, debug, dryrun):
    """Sync list files to rules"""
    # todo.py:       get_ctxobj_from_config_yamlfile()
    # -- something like ctx.obj = yaml.load(open(CONFIG_YAMLFILE_NAME).read())
    # -- may no longer need: utils.py: update_config_dict_from_pyobj(ctx.obj, config)
    # run.py:        get_dataline_list_from_listfiles(listfiles)
    # utils.py:      get_visiblefile_names_in_listdir()
    # run.py:        get_ruleobj_list_from_rule_yamlfiles()
    # run.py:        apply_rules_to_datalines(rules, data)
    # utils.py:      make_backupdir_name, then os.mkdir(backupdir)
    # todo.py:       move_existing_listfiles_to_backupdir(ctx?)
    # todo.py:       delete_older_backups()
    # run.py:        write_datadict_to_listfiles_in_currentdir(lines)
    # todo.py:       write_datadict_to_htmlfiles_in_htmldir(lines)
    # todo.py:       move_certain_listfiles_to_other_directories(ctx.obj["files2dirs"])
