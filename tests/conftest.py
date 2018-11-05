import pytest
import yaml
import click
import os
from click.testing import CliRunner
from textwrap import dedent
from mklists.rules import Rule
from mklists import (
    GLOBAL_RULES_STARTER_CONTENT,
    GLOBAL_RULEFILE_NAME,
    LOCAL_RULES_STARTER_CONTENT,
    LOCAL_RULEFILE_NAME,
    MKLISTSRC_STARTER_CONTENT,
    MKLISTSRC_LOCAL_NAME,
    MKLISTSRC_GLOBAL_NAME,
)


@pytest.fixture(name="multidir_configured")
def fixture_multidir_configured(tmpdir_factory):
    """Return temporary directory configured with:
    * .rules and mklistsrc in root directory
    * .rules in data subdirectory"""

    # Create subdir of base temp dir, return, assign to 'cwd_dir'.
    cwd_dir = tmpdir_factory.mktemp("mydir")
    mklistsrc = cwd_dir.join(MKLISTSRC_GLOBAL_NAME)
    mklistsrc.write(GLOBAL_RULES_STARTER_CONTENT)
    subdir_a = cwd_dir.mkdir("a")
    mklistsrc_a = subdir_a.join(LOCAL_RULEFILE_NAME)

    mklistsrc.write(MKLISTSRC_STARTER_CONTENT)
    another_file.write("something different")
    assert mklistsrc.read() == MKLISTSRC_STARTER_CONTENT
    assert mklistsrc_a.read() == "something different"

    # Create filehandles with basename 'cwd_dir'.
    lrules = cwd_dir.join(LOCAL_RULEFILE_NAME)
    grules = cwd_dir.join(GLOBAL_RULEFILE_NAME)
    nrules = cwd_dir.join(".local_rules")  # rule file with different name
    mklistsrc = cwd_dir.join(MKLISTSRC_LOCAL_NAME)
    mklistsrc2 = cwd_dir.join(".mklistsrc2")  # minimal .mklistsrc
    mklistsrc3 = cwd_dir.join(".mklistsrc3")  # empty .mklistsrc

    # Write to filehandles.
    lrules.write(LOCAL_RULES_STARTER_CONTENT)
    grules.write(GLOBAL_RULES_STARTER_CONTENT)
    nrules.write(LOCAL_RULES_STARTER_CONTENT)
    with open(mklistsrc, "w") as fout:
        fout.write(
            yaml.safe_dump(MKLISTSRC_STARTER_CONTENT, default_flow_style=False)
        )
    mklistsrc2.write("{ 'rules': '.local_rules' }")
    mklistsrc3.write("")

    # Return subdirectory with six new files.
    return cwd_dir


@pytest.fixture(name="singledir_configured")
def fixture_singledir_configured(tmpdir_factory):
    """Return temporary directory configured with .rules and .mklistsrc."""

    # Create subdirectory of base temp directory, return, assign to 'cwd_dir'.
    cwd_dir = tmpdir_factory.mktemp("mydir")

    # Create filehandles with basename 'cwd_dir'.
    lrules = cwd_dir.join(LOCAL_RULEFILE_NAME)
    grules = cwd_dir.join(GLOBAL_RULEFILE_NAME)
    nrules = cwd_dir.join(".local_rules")  # rule file with different name
    mklistsrc = cwd_dir.join(MKLISTSRC_LOCAL_NAME)
    mklistsrc2 = cwd_dir.join(".mklistsrc2")  # minimal .mklistsrc
    mklistsrc3 = cwd_dir.join(".mklistsrc3")  # empty .mklistsrc

    # Write to filehandles.
    lrules.write(LOCAL_RULES_STARTER_CONTENT)
    grules.write(GLOBAL_RULES_STARTER_CONTENT)
    nrules.write(LOCAL_RULES_STARTER_CONTENT)
    with open(mklistsrc, "w") as fout:
        fout.write(
            yaml.safe_dump(MKLISTSRC_STARTER_CONTENT, default_flow_style=False)
        )
    mklistsrc2.write("{ 'rules': '.local_rules' }")
    mklistsrc3.write("")

    # Return subdirectory with six new files.
    return cwd_dir


@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_was_previously_declared
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False


@pytest.fixture(scope="module")
def mklistsrc_yamlstr():
    """Return some YAML-formatted rules for writing to rule files."""

    return MKLISTSRC_STARTER_CONTENT


@pytest.fixture()
def grules_yamlstr():
    """Return some YAML-formatted rules for writing to rule files."""

    return GLOBAL_RULES_STARTER_CONTENT


@pytest.fixture()
def lrules_yamlstr():
    """Returns some YAML-formatted rules for writing to rule files."""

    return LOCAL_RULES_STARTER_CONTENT


# @pytest.fixture(scope='module')
# def rules_yamlfile(tmpdir_factory):
#    """Returns YAML-formatted file of rules."""
#
#    rules = tmpdir_factory.mktemp('datadir').join('rules')
#    print(f"Created 'rules': {repr(rules)}")
#    rules.write(dedent(lrules_yamlstr))
#    return rules


@pytest.fixture(scope="module")
def rules_bad_yamlfile(tmpdir_factory):
    """Returns badly formatted YAML rulefile object: too many fields."""

    yaml_string = """\
    - [0   , 'NOW'    , lines        , __RENAME__   , 0]
    - [0   , 'LATER'  , __RENAME__   , calendar     , 1, 5]"""

    rules = tmpdir_factory.mktemp("datadir").join("rules")
    print(f"Created 'rules': {repr(rules)}")
    rules.write(dedent(yaml_string))
    return rules


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
        Rule(
            source_matchfield=0,
            source_matchpattern=".",
            source="lines",
            target="__RENAME__",
            target_sortorder=0,
        ),
        Rule(
            source_matchfield=0,
            source_matchpattern="^= 20",
            source="__RENAME__",
            target="calendar",
            target_sortorder=1,
        ),
        Rule(
            source_matchfield=0,
            source_matchpattern="NOW",
            source="lines",
            target="__RENAME__",
            target_sortorder=0,
        ),
        Rule(
            source_matchfield=0,
            source_matchpattern="LATER",
            source="__RENAME__",
            target="calendar",
            target_sortorder=1,
        ),
    ]
