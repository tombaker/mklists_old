import click
import pytest
import os
import yaml
from click.testing import CliRunner

DEFAULTS = {'backup_dir': '.backups', 'backup_depth': 3}

with open('.config', 'w') as f:
    f.write("{'backup_dir': '.backups', 'backup_depth': 6}")

@click.command()
@click.option('--backup-dir', type=str, metavar='DIRPATH')
@click.option('--backup-depth', type=int, metavar='INTEGER')
@click.pass_context
def cli(ctx, backup_dir, backup_depth):
    overrides_from_cli = locals().copy()
    ctx.obj = DEFAULTS
    print(f"backup_depth is: {backup_depth}")
    overrides_from_file = read_overrides_from_file('.config')
    ctx.obj = apply_overrides(ctx.obj, overrides_from_file)
    ctx.obj = apply_overrides(ctx.obj, overrides_from_cli)

def read_overrides_from_file(configfile_name):
    return yaml.load(open(configfile_name).read())

def apply_overrides(context, overrides):
    overrides.pop('ctx', None)
    overrides = {key: overrides[key] for key in overrides 
                 if overrides[key] is not None}
    context.update(overrides)
    return context

@pytest.mark.cli
def test_apply_overrides():
    initial_context = {'ctx': 'something', 'datadir': '.data', 'backup_dir': '.backups', 'backup_depth': 1}
    overrides_from_file = {'backup_depth': 500}
    updated_context = apply_overrides(initial_context, overrides_from_file)
    expected_context = {'ctx': 'something', 'datadir': '.data', 'backup_dir': '.backups', 'backup_depth': 500}
    assert updated_context == expected_context

@pytest.mark.cli
def test_apply_overrides2():
    updated_context = {'ctx': 'something', 'datadir': '.data', 'backup_dir': '.backups', 'backup_depth': 500}
    overrides_from_cli = {'datadir': None, 'backup_dir': None, 'backup_depth': 1000}
    updated_context2 = apply_overrides(updated_context, overrides_from_cli)
    expected_context = {'ctx': 'something', 'datadir': '.data', 'backup_dir': '.backups', 'backup_depth': 1000}
    assert updated_context2 == expected_context

@pytest.mark.cli
def test_read_overrides_from_file(tmpdir):
    os.chdir(tmpdir)
    settings_dict = {'backup_dir': '.backups', 'backup_depth': 6}
    with open('.config', 'w') as fout:
        fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))
    assert read_overrides_from_file('.config') == settings_dict

