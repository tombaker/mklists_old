"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (MKLISTSRC_NAME, STARTER_MKLISTSRC, STARTER_GRULES, 
    STARTER_LRULES, STARTER_GRULEFILE_NAME, STARTER_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import write_initial_configfile
from glob import glob

OVERRIDE_MKLISTSRC = { 'rules': '.local_rules' }


#    # Read config file MKLISTSRC_NAME, overriding some settings in context object.
#    # -- If `mklists` was invoked with subcommand 'init', this step is skipped.
#    if ctx.invoked_subcommand != 'init':
#        update_config_from_file(
#            MKLISTSRC_NAME, 
#            givenctx_dict=ctx.obj, 
#            verbose=ctx.obj['verbose'])

@pytest.fixture(name='cwd_configured')
def fixture_cwd_configured(tmpdir_factory):
    """Return temporary directory configured with .rules and .mklistsrc."""

    # Create subdirectory of base temp directory, return, assign to 'cwd_dir'.
    cwd_dir = tmpdir_factory.mktemp('mydir')   

    # Create filehandles with basename 'cwd_dir'.
    lrules = cwd_dir.join(STARTER_LRULEFILE_NAME)
    grules = cwd_dir.join(STARTER_GRULEFILE_NAME)
    nrules = cwd_dir.join('.local_rules')

    # Write to filehandles.
    lrules.write(STARTER_LRULES)
    grules.write(STARTER_GRULES)
    nrules.write(STARTER_LRULES)

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
def test_update_config_from_file(cwd_configured):
    """@@@docstring"""
    os.chdir(cwd_configured)

def update_config_from_file(givenctx_dict=STARTER_MKLISTSRC,
                            mklistsrc=MKLISTSRC_NAME, 
                            verbose=False):
    """Returns dictionary of settings updated from configuration file.
    
    Reads configuration file from disk:
    * overrides some existing settings in the settings dictionary.
    * may add some new settings to the settings dictionary.
    * if MKLISTSRC_NAME not found, terminates with advice to run `mklists init`.

    Args:
        mklistsrc: name of configuration file - by default '.mklistsrc'.
        givenctx_dict: dictionary with setting name (key) and value.

    Returns:
        givenctx_dict: updated settings dictionary
    """
    try:
        ctx_loaded_str = yaml.load(open(mklistsrc).read())
        #given_settings = _update_config(givenctx_dict, ctx_loaded_str)
        #print(f"given_settings: {given_settings}")
        #print(f"Updated context from {repr(mklistsrc)}.")
        #if verbose:
        #    print(f"Updated context from {repr(mklistsrc)}.")
        #return givenctx_dict
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"First set up with `mklists init`.")



# 2018-10-26: Will not work unless function can return dir obj with files.
# @pytest.fixture(scope='module')
# def working_directory_with_config_files2():
#     """Return temporary working directory with .rules and .mklistsrc."""
# 
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with open(STARTER_LRULEFILE_NAME, 'w') as f:
#             f.write(STARTER_LRULES)
#         with open(MKLISTSRC_NAME, 'w') as f:
#             f.write(str(STARTER_MKLISTSRC))
#         yield



@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Tests two functions write-to-read round-trip."""
    os.chdir(tmpdir)
    configfile_name = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(
        ctxfile_name=configfile_name,
        givenctx_dict=STARTER_MKLISTSRC)
    updated_context = update_config_from_file(
        ctxfile_name=configfile_name, 
        givenctx_dict=STARTER_MKLISTSRC)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.skip
def test_update_config(tmpdir):
    context_given = { 'a': 'foo', 'b': 'bar' }
    context_from_disk = { 'b': 'baz' }
    context_expected = { 'a': 'foo', 'b': 'baz' }
    assert _update_config(context_given, context_from_disk) == context_expected

def _update_config(given_settings=None, new_settings=None):
    """Returns settings with some values overridden by new settings."""
    given_settings.update(new_settings)
    return given_settings
