import pytest
import yaml
import click
import os
from click.testing import CliRunner
from textwrap import dedent
from mklists.ruleclass import Rule
from mklists import (
    MKLISTSRC_LOCAL_NAME,
    MKLISTSRC_GLOBAL_NAME,
    MKLISTSRC_STARTER_DICT,
    RULEFILE_NAME,
    RULEFILE_STARTER_YAMLSTR,
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILEA_STARTER_YAMLSTR,
    LOCAL_RULEFILEB_STARTER_YAMLSTR,
)


@pytest.fixture(name="multidir_repo_configured")
def fixture_multidir_repo_configured(tmpdir_factory):
    """Return temporary mklists repo "mydir":
        mydir/.globalrules
        mydir/mklists.yaml
        mydir/a/.rules
        mydir/b/.rules"""

    root_dir = tmpdir_factory.mktemp("mydir")
    mklistsrc = root_dir.join(MKLISTSRC_GLOBAL_NAME)
    with open(mklistsrc, "w") as fout:
        fout.write(
            yaml.safe_dump(MKLISTSRC_STARTER_DICT, default_flow_style=False)
        )

    rules_global = root_dir.join(GLOBAL_RULEFILE_NAME)
    mklistsrc.write(GLOBAL_RULEFILE_STARTER_YAMLSTR)
    subdir_a = root_dir.mkdir("a")
    rules_a = subdir_a.join(LOCAL_RULEFILE_NAME)
    rules_a.write(LOCAL_RULEFILEA_STARTER_YAMLSTR)
    subdir_b = root_dir.mkdir("b")
    rules_b = subdir_b.join(LOCAL_RULEFILEB_NAME)
    rules_b.write(LOCAL_RULEFILEB_STARTER_YAMLSTR)
    return root_dir


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
    """Return YAML rulefile object with syntactically bad YAML.

    @@@Could this be moved into the tests themselves?"""
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
