import pytest
import os
from mklists import (MKLISTSRC, STARTER_DEFAULTS, STARTER_GLOBALRULES, 
    STARTER_GLOBALRULES, STARTER_LOCALRULES, VALID_FILENAME_CHARS)
from mklists.readwrite import (write_initial_rulefiles,
    write_initial_configfile, update_settings_from_file)


@pytest.mark.rules
def test_change_directory(tmpdir):
    os.chdir(tmpdir)
    assert str(tmpdir) == os.getcwd()

@pytest.mark.write
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(global_rules_filename='.globalrules')
    globalrules_name = tmpdir.join('.globalrules')
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(STARTER_GLOBALRULES) == globalrules_hash

@pytest.mark.write
def test_write_initial_localrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(local_rules_filename='.localrules')
    localrules_name = tmpdir.join('.localrules')
    localrules_content = open(localrules_name).read()
    localrules_hash = hash(localrules_content)
    assert hash(STARTER_LOCALRULES) == localrules_hash

@pytest.mark.write
def test_write_initial_configfile(tmpdir):
    """Tests two functions write-to-read round-trip."""
    os.chdir(tmpdir)
    mklistsrc_path = tmpdir.join(MKLISTSRC)
    write_initial_configfile(
        file_name=mklistsrc_path,
        settings_dict=STARTER_DEFAULTS)
    updated_context = update_settings_from_file(
        file_name=mklistsrc_path, 
        settings_dict=STARTER_DEFAULTS)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.init_config
def test_init_configfile():
    pass

