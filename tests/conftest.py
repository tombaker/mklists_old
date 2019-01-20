import pytest
from mklists.rules import Rule

TEST_CONFIG_YAMLFILE_NAME = "mklists.yml"
TEST_CONFIG_YAMLFILE_YAMLSTR = r"""\
invalid_filename_patterns: ['\.swp$', '\.tmp$', '~$', '^\.']
global_rules:
- [0, '.', all, lines, 0]
"""

TEST_RULE_YAMLFILEA_NAME = ".rules"
TEST_RULE_YAMLFILEA_YAMLSTR = """\
- [2, 'NOW',     lines,  now,     1]
- [2, 'LATER',   lines,  later,   0]
"""

TEST_LISTFILE_STRING = """= NOW Cook\n=LATER Read"""


@pytest.fixture(name="myrepo")
def fixture_myrepo(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    root_dir.join(TEST_CONFIG_YAMLFILE_NAME).write(TEST_CONFIG_YAMLFILE_YAMLSTR)
    subdir_a.join(TEST_RULE_YAMLFILEA_NAME).write(TEST_RULE_YAMLFILEA_YAMLSTR)
    return root_dir


@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_not_initialized_as_source
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False


@pytest.fixture(scope="module")
def ruleobj_list():
    """Returns list of Rule objects."""
    return [
        Rule(0, ".", "lines", "__RENAME__", 0),
        Rule(0, "^= 20", "__RENAME__", "calendar", 1),
        Rule(0, "NOW", "lines", "__RENAME__", 0),
        Rule(0, "LATER", "__RENAME__", "calendar", 1),
    ]
