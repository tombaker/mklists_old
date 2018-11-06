"""@@@Docstring"""

import os
import pytest
import yaml
from mklists import (
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    VALID_FILENAME_CHARS_STR,
)
from mklists.rw_init import write_initial_configfile
from mklists.readwrite import read_overrides_from_file, apply_overrides


@pytest.mark.skip
def test_apply_overrides_from_file_something_changed(singledir_configured):
    """Config file consists of just one key/value pair.
    Illustrates that .mklistsrc need not cover all mklists settings.
    Note: singledir_configured directory fixture has file '.mklistsrc2'.

    Test does not work because Python object cannot be written directly
    to '.mklistsrc2' - a step needs to be added.
    """
    os.chdir(singledir_configured)
    updated_config_dict = read_overrides_from_file(".mklistsrc2")
    print(f"verbose: {updated_config_dict['verbose']}")
    assert updated_config_dict["verbose"] != MKLISTSRC_STARTER_DICT["verbose"]


@pytest.mark.cli
def test_apply_overrides_from_file(singledir_configured):
    """apply_overrides_from_file() should return builtin settings."""
    os.chdir(singledir_configured)
    context = {}
    overrides_from_file = read_overrides_from_file(MKLISTSRC_LOCAL_NAME)
    print(apply_overrides(context, overrides_from_file))
    print(apply_overrides(context, overrides_from_file))
    assert (
        apply_overrides(context, overrides_from_file) == MKLISTSRC_STARTER_DICT
    )


@pytest.mark.cli
def test_apply_overrides():
    initial_context = {"ctx": "something", "backup_depth": 1}
    overrides_from_file = {"backup_depth": 500}
    updated_context = apply_overrides(initial_context, overrides_from_file)
    expected_context = {"ctx": "something", "backup_depth": 500}
    assert updated_context == expected_context


@pytest.mark.cli
def test_apply_overrides2():
    updated_context = {"ctx": "something", "backup_depth": 500}
    overrides_from_cli = {"backup_depth": 1000}
    updated_context2 = apply_overrides(updated_context, overrides_from_cli)
    expected_context = {"ctx": "something", "backup_depth": 1000}
    assert updated_context2 == expected_context


@pytest.mark.cli
def test_read_overrides_from_file(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {"backup_depth": 6}
    with open(".config", "w") as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert read_overrides_from_file(".config") == settings_dict
