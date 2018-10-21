import pytest
import os
from mklists import (MKLISTSRC, STARTER_DEFAULTS, STARTER_GLOBALRULES, 
    STARTER_GLOBALRULES, STARTER_LOCALRULES, VALID_FILENAME_CHARS)
from mklists.readwrite import (write_initial_rulefiles,
    write_initial_configfile, update_config_from_file, _update_config,
    write_yamlstr_to_yamlfile, read_yamlfile_parseto_pyobject)


@pytest.mark.write
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(global_rulefile_name='.globalrules')
    globalrules_name = tmpdir.join('.globalrules')
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(STARTER_GLOBALRULES) == globalrules_hash

@pytest.mark.write
def test_write_initial_localrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(local_rulefile_name='.localrules')
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
    updated_context = update_config_from_file(
        file_name=mklistsrc_path, 
        settings_dict=STARTER_DEFAULTS)
    assert updated_context['valid_filename_characters'] == VALID_FILENAME_CHARS

@pytest.mark.write
def test_update_config(tmpdir):
    context_given = { 'a': 'foo', 'b': 'bar' }
    context_from_disk = { 'b': 'baz' }
    context_expected = { 'a': 'foo', 'b': 'baz' }
    assert _update_config(context_given, context_from_disk) == context_expected

@pytest.mark.init_config
def test_init_configfile():
    pass

