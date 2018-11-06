"""@@@Docstring"""

import os
import pytest
from mklists import (
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    VALID_FILENAME_CHARS_STR,
)
from mklists.readwrite import (
    write_initial_configfile,
    read_overrides_from_file,
    apply_overrides,
)


@pytest.mark.skip
def test_apply_overrides_from_file_empty(singledir_configured):
    """Config file '.mklistsrc3' is empty (length=0)."""
    os.chdir(singledir_configured)
    updated_config_dict = apply_overrides_from_file(
        configfile_name=".mklistsrc3"
    )
    assert updated_config_dict == MKLISTSRC_DEFAULTS


@pytest.mark.skip
def test_apply_overrides_from_file_not_found(tmpdir):
    """Mklists exits if configfile is not found."""
    os.chdir(tmpdir)
    with pytest.raises(SystemExit):
        apply_overrides_from_file()


@pytest.mark.skip
def test_write_initial_configfile(tmpdir):
    """Tests that two functions correctly round-trip:
    * write_initial_configfile()
    * apply_overrides_from_file()"""
    os.chdir(tmpdir)
    mklistsrc = tmpdir.join(MKLISTSRC_NAME)
    write_initial_configfile(configfile_name=mklistsrc)
    updated_context = apply_overrides_from_file()
    assert (
        updated_context["valid_filename_characters"]
        == VALID_FILENAME_CHARS_STR
    )


@pytest.mark.skip
def test_update_config():
    """_update_config() correctly updates one dict with another."""
    context_given = {"a": "foo", "b": "bar"}
    context_from_file = {"b": "baz"}
    context_expected = {"a": "foo", "b": "baz"}
    assert _update_config(context_given, context_from_file) == context_expected
