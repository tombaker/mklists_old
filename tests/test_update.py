"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
import yaml
from mklists import (
        BUILTIN_GRULEFILE_NAME, 
        BUILTIN_GRULES, 
        BUILTIN_LRULEFILE_NAME,
        BUILTIN_LRULES, 
        BUILTIN_MKLISTSRC, 
        MKLISTSRC_NAME, 
        VALID_FILENAME_CHARS)
from mklists.readwrite import write_initial_configfile
from glob import glob


#    # Read config file MKLISTSRC_NAME, overriding some settings in context object.
#    # -- If `mklists` was invoked with subcommand 'init', this step is skipped.
#    if ctx.invoked_subcommand != 'init':
#        update_settings_from_configfile(
#            MKLISTSRC_NAME, 
#            givenctx_dict=ctx.obj, 
#            verbose=ctx.obj['verbose'])

@pytest.fixture(name='cwd_configured')
def fixture_cwd_configured(tmpdir_factory):
    """Return temporary directory configured with .rules and .mklistsrc."""

    # Create subdirectory of base temp directory, return, assign to 'cwd_dir'.
    cwd_dir = tmpdir_factory.mktemp('mydir')   

    # Create filehandles with basename 'cwd_dir'.
    lrules = cwd_dir.join(BUILTIN_LRULEFILE_NAME)
    grules = cwd_dir.join(BUILTIN_GRULEFILE_NAME)
    nrules = cwd_dir.join('.local_rules')
    mklistsrc = cwd_dir.join(MKLISTSRC_NAME)
    mklistsrc2 = cwd_dir.join('.mklistsrc2')
    mklistsrc3 = cwd_dir.join('.mklistsrc3')

    # Write to filehandles.
    lrules.write(BUILTIN_LRULES)
    grules.write(BUILTIN_GRULES)
    nrules.write(BUILTIN_LRULES)
    mklistsrc.write(BUILTIN_MKLISTSRC)
    mklistsrc2.write("{ 'rules': '.local_rules' }")
    mklistsrc3.write("")

    # Return subdirectory with three new files.
    return cwd_dir

@pytest.mark.updconfig
def test_update_config_experiment(cwd_configured):
    """@@@docstring"""
    print(type(cwd_configured))
    os.chdir(cwd_configured)
    print(os.getcwd())
    print(os.listdir())

@pytest.mark.updconfig
def test_update_settings_from_configfile(cwd_configured):
    """@@@docstring"""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile()
    print(type(BUILTIN_MKLISTSRC))
    assert updated_config_dict == BUILTIN_MKLISTSRC

@pytest.mark.updconfig
def test_update_settings_from_configfile_something_changed(cwd_configured):
    """Config file consists of just one key/value pair.
    Illustrates that .mklistsrc need not cover all mklists settings.
    Note: cwd_configured directory fixture has file '.mklistsrc2'."""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile(configfile_name='.mklistsrc2')
    assert updated_config_dict['rules'] == BUILTIN_MKLISTSRC['rules']

@pytest.mark.updconfig
def test_update_settings_from_configfile_empty(cwd_configured):
    """Config file '.mklistsrc3' is empty (length=0)."""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile(configfile_name='.mklistsrc3')
    assert updated_config_dict == BUILTIN_MKLISTSRC

def update_settings_from_configfile(builtinctx_dict=BUILTIN_MKLISTSRC,
                                    configfile_name=MKLISTSRC_NAME, 
                                    verbose=False):
    """Returns settings dict of built-ins updated from config file.
    
    Reads mklists config file from disk:
    * Settings read from file may override some of the builtin settings.
    * Handles empty config file.
    * If config file is not found, exits, advises to run `mklists init`.

    Args:
        configfile_name: name of config file, by default '.mklistsrc'.
        builtinctx_dict: dictionary with setting name (key) and value.

    Returns:
        updatedctx_dict: updated settings dictionary
    """
    try:
        loadedctx_dict = yaml.load(open(configfile_name).read())
        if not loadedctx_dict:
            loadedctx_dict = dict()
        updatedctx_dict = _update_config(builtinctx_dict, loadedctx_dict)
        if verbose:
            print(f"Updated context from {repr(configfile_name)}.")
        return updatedctx_dict
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")



# 2018-10-26: Will not work unless function can return dir obj with files.
# @pytest.fixture(scope='module')
# def working_directory_with_config_files2():
#     """Return temporary working directory with .rules and .mklistsrc."""
# 
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with open(BUILTIN_LRULEFILE_NAME, 'w') as f:
#             f.write(BUILTIN_LRULES)
#         with open(MKLISTSRC_NAME, 'w') as f:
#             f.write(str(BUILTIN_MKLISTSRC))
#         yield



@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Tests two functions write-to-read round-trip."""
    os.chdir(tmpdir)
    configfile_name = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(
        ctxfile_name=configfile_name,
        givenctx_dict=BUILTIN_MKLISTSRC)
    updated_context = update_settings_from_configfile(
                          ctxfile_name=configfile_name, 
                          givenctx_dict=BUILTIN_MKLISTSRC)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.updconfig
def test_write_initial_configfile(tmpdir):
    """Tests two functions write-to-read round-trip."""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(
        settings_dict=BUILTIN_MKLISTSRC,
        configfile_name=mklistsrc)
    updated_context = update_settings_from_configfile(
                          builtinctx_dict=BUILTIN_MKLISTSRC,
                          configfile_name=mklistsrc)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.updconfig
def test_update_config(tmpdir):
    context_given = { 'a': 'foo', 'b': 'bar' }
    context_from_disk = { 'b': 'baz' }
    context_expected = { 'a': 'foo', 'b': 'baz' }
    assert _update_config(context_given, context_from_disk) == context_expected

def _update_config(given_settings=None, new_settings=None):
    """Returns settings with some values overridden by new settings."""
    given_settings.update(new_settings)
    return given_settings
