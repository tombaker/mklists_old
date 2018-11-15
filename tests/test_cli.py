"""@@@Docstring"""

import os
import pytest
import yaml
from mklists import (
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    VALID_FILENAME_CHARACTERS_STR,
)
from mklists.cli import _read_overrides_from_file, _apply_overrides
from mklists.readwrite import write_initial_configfile

"""Things to test:
    Note: other directories in repo root created when functions called:
    * .backups/ - when @@@ is called
    * .html/    - when @@@ is called

    Note: find way to test:
    * mklistsrc2 = cwd_dir.join(".mklistsrc2")  # minimal .mklistsrc
    * mklistsrc3 = cwd_dir.join(".mklistsrc3")  # empty .mklistsrc
    Perhaps replace default .mklistsrc not here,
    but in test functions themselves:
    * mklistsrc2.write("{ 'verbose': True }")
    * mklistsrc3.write("")
    backup_dir = root_dir.mkdir(BACKUP_DIR_NAME)
    htmlfiles_dir = root_dir.mkdir(HTMLFILES_DIR_NAME)
    assert mklistsrc.read() == MKLISTSRC_STARTER_DICT
    Note: .globalrules and .rules should never exist in same directory:
    * .globalrules always one level up.
    What about:
    * mklistsrc2.write("{ 'rules': '.local_rules' }")
    * mklistsrc3.write("")
"""


@pytest.mark.skip
def test_apply_overrides_from_file_something_changed(singledir_configured):
    """Config file consists of just one key/value pair.
    Illustrates that .mklistsrc need not cover all mklists settings.
    Note: singledir_configured directory fixture has file '.mklistsrc2'.

    Test does not work because Python object cannot be written directly
    to '.mklistsrc2' - a step needs to be added.
    """
    os.chdir(singledir_configured)
    updated_config_dict = _read_overrides_from_file(".mklistsrc2")
    print(f"verbose: {updated_config_dict['verbose']}")
    assert updated_config_dict["verbose"] != MKLISTSRC_STARTER_DICT["verbose"]


@pytest.mark.skip
def test_apply_overrides_from_file(singledir_configured):
    """_apply_overrides_from_file() should return builtin settings."""
    os.chdir(singledir_configured)
    context = {}
    overrides_from_file = _read_overrides_from_file(MKLISTSRC_LOCAL_NAME)
    print(_apply_overrides(context, overrides_from_file))
    print(_apply_overrides(context, overrides_from_file))
    assert (
        _apply_overrides(context, overrides_from_file)
        == MKLISTSRC_STARTER_DICT
    )


@pytest.mark.cli
def test_apply_overrides():
    initial_context = {"ctx": "something", "backups": 1}
    overrides_from_file = {"backups": 500}
    updated_context = _apply_overrides(initial_context, overrides_from_file)
    expected_context = {"ctx": "something", "backups": 500}
    assert updated_context == expected_context


@pytest.mark.cli
def test_apply_overrides2():
    updated_context = {"ctx": "something", "backups": 500}
    overrides_from_cli = {"backups": 1000}
    updated_context2 = _apply_overrides(updated_context, overrides_from_cli)
    expected_context = {"ctx": "something", "backups": 1000}
    assert updated_context2 == expected_context


@pytest.mark.cli
def test_read_overrides_from_file(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {"backups": 6}
    with open(".config", "w") as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert _read_overrides_from_file(".config") == settings_dict


@pytest.mark.skip
def test_apply_overrides_from_file_empty(singledir_configured):
    """Config file '.mklistsrc3' is empty (length=0)."""
    os.chdir(singledir_configured)
    updated_config_dict = _apply_overrides_from_file(
        configfile_name=".mklistsrc3"
    )
    assert updated_config_dict == MKLISTSRC_DEFAULTS


@pytest.mark.skip
def test_apply_overrides_from_file_not_found(tmpdir):
    """Mklists exits if configfile is not found."""
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        _apply_overrides_from_file()


@pytest.mark.skip
def test_update_config():
    """_update_config() correctly updates one dict with another."""
    context_given = {"a": "foo", "b": "bar"}
    context_from_file = {"b": "baz"}
    context_expected = {"a": "foo", "b": "baz"}
    assert _update_config(context_given, context_from_file) == context_expected
