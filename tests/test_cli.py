"""@@@Docstring"""

import os
import pytest
import yaml
from mklists import (
    BUILTIN_MKLISTSRC,
    MKLISTSRC_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import (
    write_initial_configfile,
    read_overrides_from_file,
    apply_overrides)


@pytest.mark.cli
def test_apply_overrides_from_file(cwd_configured):
    """apply_overrides_from_file() should return builtin settings."""
    os.chdir(cwd_configured)
    context = {}
    overrides_from_file = read_overrides_from_file(MKLISTSRC_NAME)
    print(apply_overrides(context, overrides_from_file))
    print(apply_overrides(context, overrides_from_file))
    assert apply_overrides(context, overrides_from_file) == BUILTIN_MKLISTSRC


@pytest.mark.cli
def test_apply_overrides():
    initial_context = {
        'ctx': 'something',
        'datadir': '.data',
        'backup_dir': '.backups',
        'backup_depth': 1}
    overrides_from_file = {'backup_depth': 500}
    updated_context = apply_overrides(initial_context, overrides_from_file)
    expected_context = {
        'ctx': 'something',
        'datadir': '.data',
        'backup_dir': '.backups',
        'backup_depth': 500}
    assert updated_context == expected_context


@pytest.mark.cli
def test_apply_overrides2():
    updated_context = {
        'ctx': 'something',
        'datadir': '.data',
        'backup_dir': '.backups',
        'backup_depth': 500}
    overrides_from_cli = {
        'datadir': None,
        'backup_dir': None,
        'backup_depth': 1000}
    updated_context2 = apply_overrides(updated_context, overrides_from_cli)
    expected_context = {
        'ctx': 'something',
        'datadir': '.data',
        'backup_dir': '.backups',
        'backup_depth': 1000}
    assert updated_context2 == expected_context


@pytest.mark.cli
def test_read_overrides_from_file(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {'backup_dir': '.backups', 'backup_depth': 6}
    with open('.config', 'w') as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert read_overrides_from_file('.config') == settings_dict
