import pytest
from mklists.rules import Rule
from mklists import CONFIGFILE_NAME, CONFIGFILE_YAMLSTR, LOCAL_RULEFILE_NAME

TEST_RULEFILEA_YAMLSTR = """\
- [0, '.',       lines,     todo.txt,    0]
- [0, '.',       to_a.txt   todo.txt,    1]
- [2, 'NOW',     todo.txt,  now.txt,     1]
- [2, 'LATER',   todo.txt,  later.txt,   0]
"""

TEST_RULEFILEB_YAMLSTR = """\
- [0, '.',       lines,     other.txt,   1]
- [0, '.',       to_b.txt,  other.txt,   1]
- [2, 'SOMEDAY', other.txt, someday.txt, 0]
"""


@pytest.fixture(name="myrepo_configured")
def fixture_myrepo_configured(tmpdir_factory):
    """Return temporary mklists repo 'myrepo'."""
    root_dir = tmpdir_factory.mktemp("myrepo")
    subdir_a = root_dir.mkdir("a")
    subdir_b = root_dir.mkdir("b")
    root_dir.join(CONFIGFILE_NAME).write(CONFIGFILE_YAMLSTR)
    subdir_a.join(LOCAL_RULEFILE_NAME).write(TEST_RULEFILEA_YAMLSTR)
    subdir_b.join(LOCAL_RULEFILE_NAME).write(TEST_RULEFILEB_YAMLSTR)
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
