import os
from textwrap import dedent
import pytest
import yaml
from mklists.rules import Rule
from mklists import CONFIGFILE_NAME, CONFIG_STARTER_DICT, LOCAL_RULEFILE_NAME

TEST_GLOBAL_DIR = "."
TEST_GLOBAL_RULES_FROM_MKLISTSYML = """\
- [0, '^=',       all_lines, to_a.txt, 1]
- [0, '^201[89]', all_lines, to_b.txt, 1]
"""

TEST_LOCAL_DIRA = os.path.join(TEST_GLOBAL_DIR, "todo")
TEST_LOCAL_RULEFILEA_STARTER_YAMLSTR = """\
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       to_a.txt    todo.txt,   1]
- [2, 'NOW',     todo.txt,    now.txt,   1]
- [2, 'LATER',   todo.txt,  later.txt,   0]
"""
TEST_LOCAL_DIRB = os.path.join(TEST_GLOBAL_DIR, "log")
TEST_LOCAL_RULEFILEB_STARTER_YAMLSTR = """\
- [0, '.',           lines,   other.txt, 1]
- [0, '.',        to_b.txt,   other.txt, 1]
- [2, 'SOMEDAY', other.txt, someday.txt, 0]
"""


@pytest.fixture(name="myrepo_configured")
def fixture_myrepo_configured(tmpdir_factory):
    """Return temporary mklists repo "myrepo":

        myrepo/mklists.yml
        myrepo/a/.rules
        myrepo/b/.rules"""

    root_dir = tmpdir_factory.mktemp("myrepo")
    mklistsrc = root_dir.join(CONFIGFILE_NAME)
    with open(mklistsrc, "w") as fout:
        fout.write(yaml.safe_dump(CONFIG_STARTER_DICT, default_flow_style=False))

    # get global rules from mklists.yml
    subdir_a = root_dir.mkdir("a")
    rules_a = subdir_a.join(LOCAL_RULEFILE_NAME)
    rules_a.write(TEST_LOCAL_RULEFILEA_STARTER_YAMLSTR)
    subdir_b = root_dir.mkdir("b")
    rules_b = subdir_b.join(LOCAL_RULEFILE_NAME)
    rules_b.write(TEST_LOCAL_RULEFILEB_STARTER_YAMLSTR)
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
