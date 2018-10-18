import pytest
import os
from mklists import (MKLISTSRC, STARTER_DEFAULTS, STARTER_GLOBALRULES, 
    STARTER_GLOBALRULES, STARTER_LOCALRULES)
from mklists.readwrite import (write_initial_rulefiles,
    write_initial_configfile, load_mklistsrc)


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
    os.chdir(tmpdir)
    mklistsrc_path = tmpdir.join(MKLISTSRC)
    write_initial_configfile(filename=mklistsrc_path,
                             context=STARTER_DEFAULTS)
    ctx = load_mklistsrc(mklistsrc_path, context=STARTER_DEFAULTS)
    assert ctx['VALID_FILENAME_CHARS'] == VALID_FILENAME_CHARS

@pytest.mark.init_config
def test_init_configfile():
    pass

