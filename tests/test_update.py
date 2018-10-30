"""@@@Docstring"""

import os
import pytest
from mklists import (
    BUILTIN_MKLISTSRC,
    MKLISTSRC_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import (
    write_initial_configfile,
    update_settings_from_configfile,
    _update_config)


@pytest.mark.updconfig
def test_update_settings_from_configfile(cwd_configured):
    """update_settings_from_configfile() should return builtin settings."""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile()
    assert updated_config_dict == BUILTIN_MKLISTSRC


@pytest.mark.updconfig
def test_update_settings_from_configfile_something_changed(cwd_configured):
    """Config file consists of just one key/value pair.
    Illustrates that .mklistsrc need not cover all mklists settings.
    Note: cwd_configured directory fixture has file '.mklistsrc2'."""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile(
        configfile_name='.mklistsrc2')
    assert updated_config_dict['rules'] == BUILTIN_MKLISTSRC['rules']


@pytest.mark.updconfig
def test_update_settings_from_configfile_empty(cwd_configured):
    """Config file '.mklistsrc3' is empty (length=0)."""
    os.chdir(cwd_configured)
    updated_config_dict = update_settings_from_configfile(
        configfile_name='.mklistsrc3')
    assert updated_config_dict == BUILTIN_MKLISTSRC


@pytest.mark.updconfig
def test_update_settings_from_configfile_not_found(tmpdir):
    """Mklists exits if configfile is not found."""
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        update_settings_from_configfile()


@pytest.mark.updconfig
def test_write_initial_configfile(tmpdir):
    """Tests that two functions correctly round-trip:
    * write_initial_configfile()
    * update_settings_from_configfile()"""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(configfile_name=mklistsrc)
    updated_context = update_settings_from_configfile()
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS


@pytest.mark.updconfig
def test_update_config():
    """_update_config() correctly updates one dict with another."""
    context_given = {'a': 'foo', 'b': 'bar'}
    context_from_disk = {'b': 'baz'}
    context_expected = {'a': 'foo', 'b': 'baz'}
    assert _update_config(context_given, context_from_disk) == context_expected
