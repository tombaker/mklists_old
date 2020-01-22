"""@@@Docstring"""

import pytest
from mklists.rules import Rule
from mklists.constants import CONFIG_YAMLFILE_NAME, RULES_CSVFILE_NAME


@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_filename_field_was_properly_initialized
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False


@pytest.fixture(name="myrepo")
def fixture_myrepo(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    # pylint: disable=unused-variable
    # Not a problem; this is just a fixture.
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    root_dir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
    root_dir.join(RULES_CSVFILE_NAME).write("rule stuff")
    subdir_a.join(RULES_CSVFILE_NAME).write("rule stuff")
    subdir_b = subdir_a.mkdir("b")
    subdir_b.mkdir("c")
    return root_dir
