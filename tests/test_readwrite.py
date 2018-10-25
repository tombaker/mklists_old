"""@@@Docstring"""

import pytest
import click
from click.testing import CliRunner
import os
from mklists import (MKLISTSRC_NAME, STARTER_MKLISTSRC, STARTER_GRULES, 
    STARTER_LRULES, STARTER_GRULEFILE_NAME, STARTER_LRULEFILE_NAME,
    VALID_FILENAME_CHARS)
from mklists.readwrite import (write_initial_rulefiles,
    write_initial_configfile, write_yamlstr_to_yamlfile, 
    read_yamlfile_parseto_pyobject)


@pytest.mark.write
def test_write_initial_globalrules_isolated():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write_initial_rulefiles(
            global_rulefile_name=STARTER_GRULEFILE_NAME,
            globalrules_content=STARTER_GRULES)
        assert STARTER_GRULES == open(STARTER_GRULEFILE_NAME).read()

@pytest.mark.write
def test_write_initial_globalrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(global_rulefile_name='.globalrules')
    globalrules_name = tmpdir.join('.globalrules')
    globalrules_content = open(globalrules_name).read()
    globalrules_hash = hash(globalrules_content)
    assert hash(STARTER_GRULES) == globalrules_hash

@pytest.mark.write
def test_write_initial_localrules(tmpdir):
    os.chdir(tmpdir)
    write_initial_rulefiles(local_rulefile_name='.localrules')
    localrules_name = tmpdir.join('.localrules')
    localrules_content = open(localrules_name).read()
    localrules_hash = hash(localrules_content)
    assert hash(STARTER_LRULES) == localrules_hash

