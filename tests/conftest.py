import pytest
from mklists.rules import Rule

TEST_CONFIGFILE_NAME = "mklists.yml"
TEST_CONFIGFILE_YAMLSTR = r"""\
invalid_filename_patterns: ['\.swp$', '\.tmp$', '~$', '^\.']
global_rules:
- [0, '.', all, lines, 0]
"""

TEST_RULEFILEA_NAME = ".rules"
TEST_RULEFILEA_YAMLSTR = """\
- [2, 'NOW',     lines,  now,     1]
- [2, 'LATER',   lines,  later,   0]
"""

TEST_RULEFILEB_NAME = ".localrules"
TEST_RULEFILEB_YAMLSTR = """\
- [2, 'NOW',     lines,  now,     1]
- [2, 'LATER',   lines,  later,   0]
"""

TEST_LISTFILE_STRING = """= NOW Cook\n=LATER Read"""


@pytest.fixture(name="myrepo_configured")
def fixture_myrepo_configured(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    subdir_b = root_dir.mkdir("b")
    root_dir.join(TEST_CONFIGFILE_NAME).write(TEST_CONFIGFILE_YAMLSTR)
    subdir_a.join(TEST_RULEFILEA_NAME).write(TEST_RULEFILEA_YAMLSTR)
    subdir_b.join(TEST_RULEFILEB_NAME).write(TEST_RULEFILEB_YAMLSTR)
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
def ruleobjs_list():
    """Returns list of Rule objects."""
    return [
        Rule(0, ".", "lines", "__RENAME__", 0),
        Rule(0, "^= 20", "__RENAME__", "calendar", 1),
        Rule(0, "NOW", "lines", "__RENAME__", 0),
        Rule(0, "LATER", "__RENAME__", "calendar", 1),
    ]
