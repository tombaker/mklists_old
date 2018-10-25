"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (MKLISTSRC_NAME, STARTER_MKLISTSRC, STARTER_GRULES, 
    STARTER_LRULES, STARTER_GRULEFILE_NAME, STARTER_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import write_initial_configfile


def update_config_from_file(file_name=MKLISTSRC_NAME, 
                            settings_dict=STARTER_MKLISTSRC,
                            verbose=False):
    """Returns dictionary of settings updated from configuration file.
    
    Reads configuration file from disk:
    * overrides some existing settings in the settings dictionary.
    * may add some new settings to the settings dictionary.
    * if MKLISTSRC_NAME not found, terminates with advice to run `mklists init`.

    Args:
        file_name: name of configuration file - by default '.mklistsrc'.
        settings_dict: dictionary with setting name (key) and value.

    Returns:
        settings_dict: updated settings dictionary
    """
    try:
        print('Hello, world!')
        #print(yaml.load(open(file_name).read()))
        #settings_loaded_str = yaml.load(open(file_name).read())
        #print(f"settings_loaded_str: {settings_loaded_str}")
        #given_settings = _update_config(settings_dict, settings_loaded_str)
        #print(f"given_settings: {given_settings}")
        #print(f"Updated context from {repr(file_name)}.")
        #if verbose:
        #    print(f"Updated context from {repr(file_name)}.")
        #return settings_dict
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")

def _update_config(given_settings=None, loaded_settings=None):
    given_settings.update(loaded_settings)
    return given_settings



@pytest.fixture()
def working_directory_with_config_files(tmpdir):
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
def working_directory_with_config_files():
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
    mklistsrc_path = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(
        file_name=mklistsrc_path,
        settings_dict=STARTER_MKLISTSRC)
    updated_context = update_config_from_file(
        file_name=mklistsrc_path, 
        settings_dict=STARTER_MKLISTSRC)
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
            settings_dict=ctx.obj, 
            verbose=ctx.obj['verbose'])

