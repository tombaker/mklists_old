"""CLI - command-line interface module"""

import click

# from .run import (
#    get_ruleobj_list_from_rule_yamlfiles,
#    get_dataline_list_from_listfiles,
#    apply_rules_to_datalines,
#    write_datadict_to_listfiles_in_currentdir,
#    write_datadict_to_htmlfiles_in_htmldir,
#    move_existing_listfiles_to_backupdir,
#    move_certain_listfiles_to_other_directories,
# )


@click.group()
@click.version_option("0.1.5", help="Show version and exit.")
@click.help_option(help="Show help and exit.")
@click.pass_context
def cli(ctx):
    """Organize your todo lists by tweaking rules"""


@cli.command()
@click.option("--empty", is_flag=True, help="Minimal configuration (for experts).")
@click.pass_context
def init(ctx, empty):
    """Write starter configuration and rule files."""
    # initialize_config_yamlfiles()
    # write_initial_rule_yamlfiles()


@cli.command()
@click.option("--debug", is_flag=True, help="Run verbosely.")
@click.option("--dryrun", is_flag=True, help="Run verbosely in read-only mode.")
@click.pass_context
def run(ctx, debug, dryrun):
    """Apply rules to re-write data files."""
    # RUN   get_ctxobj_from_config_yamlfile()
    # RUN   -- something like ctx.obj = yaml.load(open(CONFIG_YAMLFILE_NAME).read())
    # RUN   -- may no longer need: update_config_dict_from_pyobj(ctx.obj, config)
    # RUN   get_dataline_list_from_listfiles(listfiles)
    # RUN   get_listfile_names()
    # RUN   get_ruleobj_list_from_rule_yamlfiles()
    # RUN   apply_rules_to_datalines(rules, data)
    # RUN   make_backupdir_name, then os.mkdir(backupdir)
    # RUN   move_existing_listfiles_to_backupdir(ctx?)
    # RUN   delete_older_backups()
    # RUN   write_datadict_to_listfiles_in_currentdir(lines)
    # RUN   write_datadict_to_htmlfiles_in_htmldir(lines)
    # RUN   move_certain_listfiles_to_other_directories(ctx.obj["files2dirs"])
