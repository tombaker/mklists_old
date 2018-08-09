import os
import re
import glob

import click
from dataclasses import dataclass
from configparser import ConfigParser


@click.group()
@click.option(
    '--config', 
    default='.mklistsrc', 
    metavar='FILENAME', 
    help="Configuration file.")
@click.option(
    '--rules', 
    default='.rules', 
    metavar='FILENAME', 
    help="Rule file, repeatable.")
@click.option(
    '--data-folder', 
    default='.', 
    metavar='DIRNAME', 
    help="Data folder.")
@click.option(
    '--html-folder', 
    default='.html', 
    metavar='DIRNAME', 
    help="Data folder, urlified.")
@click.option(
    '--backup-folder', 
    default='.backups', 
    metavar='DIRNAME', 
    help="Backup folder.")
@click.option(
    '--backup-depth', 
    default=3, 
    help="Backup depth.")
@click.option(
    '--verbose', 
    default=False, 
    is_flag=True,
    help="Run in verbose mode.")
@click.version_option('0.2', help="Show version and exit.")
@click.pass_context
def cli(ctx, config, rules, data_folder, html_folder, backup_folder, 
        backup_depth, verbose):
    """Manage plain text lists by tweaking rules"""
    print("Before reading config file: backup_depth =", backup_depth)
    mklrc = ConfigParser()
    mklrc.read('.mklistsrc')
    mklistsrc = dict([[key, mklrc['DEFAULTS'][key]] for key in mklrc['DEFAULTS']])
    print("Values as read from config file: mklistsrc = ", mklistsrc)  ################
    ctx.obj = mklistsrc
    print("After reading values from config file: ctx.obj = ", ctx.obj)  ################

    if config:
        ctx.obj['config'] = config

    if rules:
        ctx.obj['rules'] = rules

    if data_folder:
        ctx.obj['data_folder'] = data_folder

    if html_folder:   
        ctx.obj['html_folder'] = html_folder

    if backup_folder:
        ctx.obj['backup_folder'] = backup_folder

    if backup_depth:
        ctx.obj['backup_depth'] = backup_depth

    if verbose:
        ctx.obj['verbose'] = verbose

    print("ctx.obj = ", ctx.obj)  ################ 12345
    print("After overriding with values set on command line: ctx.obj['data_folder'] =", repr(ctx.obj['data_folder']))  #######
    #click.echo(f'>>> ctx.obj.backup_depth      =>  {ctx.obj.backup_depth}') #####


@cli.command()
@click.pass_context
def init(list_folder):
    """Initialize folder for Mklists data."""
    print('@@@TODO')

@cli.command()
@click.pass_context
def make(ctx):
    """Regenerate lists according to rules."""
    click.echo(f'>>> ctx                             =>  {ctx}')
    click.echo(f'>>> ctx.obj                        =>  {ctx.obj}')
    click.echo(f'>>> ctx.obj["rules"]               =>  {ctx.obj["rules"]}')
    #click.echo(f'>>> ctx.__dir__()...              =>  {[item for item in ctx.__dir__() if not re.search("__", item)]}')
    #click.echo(f'>>> ctx.list_folder               =>  {ctx.list_folder}')
    #click.echo(f'>>> ctx.backup_folder             =>  {ctx.backup_folder}')
    #click.echo(f'>>> ctx.backup_depth              =>  {ctx.backup_depth}')
    #click.echo(f'>>> ctx.html_folder               =>  {ctx.html_folder}')
    #click.echo(f'>>> ctx.verbose                   =>  {ctx.verbose}')
    #click.echo(f'>>> ctx.get_config                =>  {ctx.get_config}')
    #click.echo()

@cli.command()
@click.pass_context
def check(ctx):
    """Dry-run with verbose sanity checks."""
    # Print to screen all (non-dunder) config attributes/values

@cli.command()
@click.pass_context
def rules(ctx):
    """Inspect rules."""
    # Print to screen all (non-dunder) config attributes/values

