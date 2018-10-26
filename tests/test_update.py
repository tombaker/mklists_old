"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (MKLISTSRC_NAME, STARTER_MKLISTSRC, STARTER_GRULES, 
    STARTER_LRULES, STARTER_GRULEFILE_NAME, STARTER_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import write_initial_configfile

NEW_MKLISTSRC = { 'rules': '.local_rules' }


def update_config_from_file(ctxfile_name=MKLISTSRC_NAME, 
                            ctx_dict=STARTER_MKLISTSRC,
                            verbose=False):
    """Returns dictionary of settings updated from configuration file.
    
    Reads configuration file from disk:
    * overrides some existing settings in the settings dictionary.
    * may add some new settings to the settings dictionary.
    * if MKLISTSRC_NAME not found, terminates with advice to run `mklists init`.

    Args:
        ctxfile_name: name of configuration file - by default '.mklistsrc'.
        ctx_dict: dictionary with setting name (key) and value.

    Returns:
        ctx_dict: updated settings dictionary
    """
    try:
        print('Hello, world!')
        #print(yaml.load(open(ctxfile_name).read()))
        #settings_loaded_str = yaml.load(open(ctxfile_name).read())
        #print(f"settings_loaded_str: {settings_loaded_str}")
        #given_settings = _update_config(ctx_dict, settings_loaded_str)
        #print(f"given_settings: {given_settings}")
        #print(f"Updated context from {repr(ctxfile_name)}.")
        #if verbose:
        #    print(f"Updated context from {repr(ctxfile_name)}.")
        #return ctx_dict
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")



@pytest.fixture(name='working_directory_with_config_files1')
def fixture_working_directory_with_config_files1(tmpdir):
    """Return temporary working directory with .rules and .mklistsrc."""

    os.getcwd()
    os.chdir(tmpdir)
    lrules = tmpdir.join(STARTER_LRULEFILE_NAME)
    grules = tmpdir.join(STARTER_GRULEFILE_NAME)
    nrules = tmpdir.join('.local_rules')
    lrules.write(STARTER_LRULES)
    grules.write(STARTER_GRULES)
    nrules.write(STARTER_LRULES)
    return tmpdir

@pytest.fixture(scope='module')
def working_directory_with_config_files2():
    """Return temporary working directory with .rules and .mklistsrc."""

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(STARTER_LRULEFILE_NAME, 'w') as f:
            f.write(STARTER_LRULES)
        with open(MKLISTSRC_NAME, 'w') as f:
            f.write(str(STARTER_MKLISTSRC))
        yield



@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Tests two functions write-to-read round-trip."""
    os.chdir(tmpdir)
    configfile_name = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(
        ctxfile_name=configfile_name,
        ctx_dict=STARTER_MKLISTSRC)
    updated_context = update_config_from_file(
        ctxfile_name=configfile_name, 
        ctx_dict=STARTER_MKLISTSRC)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.skip
def test_update_config(tmpdir):
    context_given = { 'a': 'foo', 'b': 'bar' }
    context_from_disk = { 'b': 'baz' }
    context_expected = { 'a': 'foo', 'b': 'baz' }
    assert _update_config(context_given, context_from_disk) == context_expected

    # Read config file MKLISTSRC_NAME, overriding some settings in context object.
    # -- If `mklists` was invoked with subcommand 'init', this step is skipped.
    if ctx.invoked_subcommand != 'init':
        update_config_from_file(
            MKLISTSRC_NAME, 
            ctx_dict=ctx.obj, 
            verbose=ctx.obj['verbose'])

def _update_config(given_settings=None, new_settings=None):
    """Returns settings with some values overridden by new settings."""
    given_settings.update(new_settings)
    return given_settings
