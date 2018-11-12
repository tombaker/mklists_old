import pytest
import yaml
import click
import os
from click.testing import CliRunner
from textwrap import dedent
from mklists.rules import Rule
from mklists import (
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    RULEFILE_NAME,
    RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILEA_STARTER_YAMLSTR,
    LOCAL_RULEFILEB_STARTER_YAMLSTR,
    MKLISTSRC_STARTER_DICT,
    MKLISTSRC_LOCAL_NAME,
    MKLISTSRC_GLOBAL_NAME,
    BACKUP_DIR_NAME,
    HTMLFILES_DIR_NAME,
)


@pytest.fixture(name="multidir_configured")
def fixture_multidir_configured(tmpdir_factory):
    """Return temporary mklists "repo" configured with:
    * files .globalrules and mklistsrc in root directory
    * file .rules in data subdirectory
    Note: other directories in repo root created when functions called:
    * .backups/ - when @@@ is called
    * .html/    - when @@@ is called

    Note: find way to test:
    * mklistsrc2 = cwd_dir.join(".mklistsrc2")  # minimal .mklistsrc
    * mklistsrc3 = cwd_dir.join(".mklistsrc3")  # empty .mklistsrc
    Perhaps replace default .mklistsrc not here,
    but in test functions themselves:
    * mklistsrc2.write("{ 'verbose': True }")
    * mklistsrc3.write("")"""

    # Create subdir of (temporary) base directory and assign to 'root_dir'.
    root_dir = tmpdir_factory.mktemp("mydir")
    mklistsrc = root_dir.join(MKLISTSRC_GLOBAL_NAME)
    with open(mklistsrc, "w") as fout:
        fout.write(
            yaml.safe_dump(MKLISTSRC_STARTER_DICT, default_flow_style=False)
        )

    # .globalrules
    rules_global = root_dir.join(GLOBAL_RULEFILE_NAME)
    mklistsrc.write(GLOBAL_RULEFILE_STARTER_YAMLSTR)

    # a/.rules
    subdir_a = root_dir.mkdir("a")
    rules_a = subdir_a.join(LOCAL_RULEFILE_NAME)
    rules_a.write(LOCAL_RULEFILEA_STARTER_YAMLSTR)

    # b/.rules
    subdir_b = root_dir.mkdir("b")
    rules_b = subdir_b.join(LOCAL_RULEFILEB_NAME)
    rules_b.write(LOCAL_RULEFILEB_STARTER_YAMLSTR)

    backup_dir = root_dir.mkdir(BACKUP_DIR_NAME)
    htmlfiles_dir = root_dir.mkdir(HTMLFILES_DIR_NAME)

    assert mklistsrc.read() == MKLISTSRC_STARTER_DICT

    # Return subdirectory with four new files.
    return root_dir


@pytest.fixture(name="singledir_configured")
def fixture_singledir_configured(tmpdir_factory):
    """Return temporary directory configured with .rules and .mklistsrc.

    Note: .globalrules and .rules should never exist in same directory:
    * .globalrules always one level up.

    What about:
    * mklistsrc2.write("{ 'rules': '.local_rules' }")
    * mklistsrc3.write("")
    """

    # Create (temporary) subdir of base temp directory, assign to 'cwd_dir'.
    cwd_dir = tmpdir_factory.mktemp("mydir")

    # Create filehandles with basename 'cwd_dir'.
    rules = cwd_dir.join(RULEFILE_NAME)
    mklistsrc = cwd_dir.join(MKLISTSRC_LOCAL_NAME)

    # Write to filehandles.
    rules.write(RULEFILE_STARTER_YAMLSTR)
    with open(mklistsrc, "w") as fout:
        fout.write(
            yaml.safe_dump(MKLISTSRC_STARTER_DICT, default_flow_style=False)
        )

    # Return subdirectory with six new files.
    return cwd_dir


@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_was_properly_registered
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False


@pytest.fixture(scope="module")
def rules_bad_yamlfile2(tmpdir_factory):
    """Returns badly formatted YAML rulefile object: bad YAML syntax."""

    yaml_rule_data = """- [1, 2, 3, 4]\n+ [5, 6, 7, 8]"""
    some_yamlfile = tmpdir_factory.mktemp("datadir").join("some_yamlfile")
    print(f"Created 'some_yamlfile': {repr(some_yamlfile)}")
    some_yamlfile.write(dedent(yaml_rule_data))
    return some_yamlfile


@pytest.fixture(scope="module")
def rules_python():
    """Returns list of Rule objects."""
    return [
        Rule(0, ".", "lines", "__RENAME__", 0),
        Rule(0, "^= 20", "__RENAME__", "calendar", 1),
        Rule(0, "NOW", "lines", "__RENAME__", 0),
        Rule(0, "LATER", "__RENAME__", "calendar", 1),
    ]
