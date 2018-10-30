"""@@@Docstring"""

import os
import pytest
import yaml
from mklists import (
    BUILTIN_GRULEFILE_NAME,
    BUILTIN_GRULES,
    BUILTIN_LRULEFILE_NAME,
    BUILTIN_LRULES,
    BUILTIN_MKLISTSRC,
    MKLISTSRC_NAME,
    VALID_FILENAME_CHARS,
    ConfigFileNotFoundError)
from mklists.readwrite import (
    write_initial_configfile,
    update_settings_from_configfile,
    _update_config)


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
def test_update_config():
    """@@@docstring"""
    context_given = {'a': 'foo', 'b': 'bar'}
    context_from_disk = {'b': 'baz'}
    context_expected = {'a': 'foo', 'b': 'baz'}
    assert _update_config(context_given, context_from_disk) == context_expected
