import pytest
import os
from mklists import (MKLISTSRC, STARTER_GLOBALRULES, 
    STARTER_GLOBALRULES, STARTER_LOCALRULES)
from mklists.readwrite import write_initial_rulefiles


@pytest.mark.tmpdir
def test_change_directory(tmpdir):
    os.chdir(tmpdir)
    assert str(tmpdir) == os.getcwd()

@pytest.mark.tmpdir
def test_write_initial_rules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(global_rules_filename='.globalrules')
    globalrules_name = tmpdir.join('.globalrules')
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(STARTER_GLOBALRULES) == globalrules_hash

@pytest.mark.init_config
def test_init_configfile():
    pass

