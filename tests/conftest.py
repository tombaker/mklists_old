import pytest
import yaml
from textwrap import dedent
from mklists.rule import Rule

@pytest.fixture()
def reinitialize_ruleclass_variables():
    """Class variables must be re-initialized:
        for each test of Rule.isrule
        for each test of x._source_is_precedented
        for each test of Rule.sources_list"""
    Rule.sources_list = []
    Rule.sources_list_is_initialized = False

@pytest.fixture(scope='module')
def grules_yamlstr(tmpdir_factory):
    """Return some YAML-formatted rules for writing to YAML rule files."""

    return """\
    - [0,  '.'        , lines        , __RENAME__   , 0]
    - [0,  '^= 20'    , __RENAME__   , calendar     , 1]"""

@pytest.fixture(scope='module')
def lrules_yamlstr(tmpdir_factory):
    """Return some YAML-formatted rules for writing to YAML rule files."""

    return """\
    - [0   , 'NOW'    , lines        , __RENAME__   , 0]
    - [0   , 'LATER'  , __RENAME__   , calendar     , 1]"""

@pytest.fixture(scope='module')
def rules_yamlfile(tmpdir_factory):
    """Return YAML-formatted file of rules."""

    yaml_string = """\
    - [0   , 'NOW'    , lines        , __RENAME__   , 0]
    - [0   , 'LATER'  , __RENAME__   , calendar     , 1]"""

    rules = tmpdir_factory.mktemp('datadir').join('rules')
    print(f"Created 'rules': {repr(rules)}")
    rules.write(dedent(yaml_string))
    return rules

@pytest.fixture(scope='module')
def rules_bad_yamlfile(tmpdir_factory):
    """Returns bad YAML rulefile object: too many fields."""

    yaml_string = """\
    - [0   , 'NOW'    , lines        , __RENAME__   , 0]
    - [0   , 'LATER'  , __RENAME__   , calendar     , 1, 5]"""

    rules = tmpdir_factory.mktemp('datadir').join('rules')
    print(f"Created 'rules': {repr(rules)}")
    rules.write(dedent(yaml_string))
    return rules

@pytest.fixture(scope='module')
def rules_bad_yamlfile2(tmpdir_factory):
    """Returns bad YAML rulefile object: bad YAML syntax."""

    yaml_rule_data = """- [1, 2, 3, 4]\n+ [5, 6, 7, 8]"""
    some_yamlfile = tmpdir_factory.mktemp('datadir').join('some_yamlfile')
    print(f"Created 'some_yamlfile': {repr(some_yamlfile)}")
    some_yamlfile.write(dedent(yaml_rule_data))
    return some_yamlfile

@pytest.fixture(scope='module')
def rules_python():
    """docstring@@@"""
    return [
                Rule(source_matchfield=0, source_matchpattern='.', source='lines', target='__RENAME__', target_sortorder=0),
                Rule(source_matchfield=0, source_matchpattern='^= 20', source='__RENAME__', target='calendar', target_sortorder=1),
                Rule(source_matchfield=0, source_matchpattern='NOW', source='lines', target='__RENAME__', target_sortorder=0),
                Rule(source_matchfield=0, source_matchpattern='LATER', source='__RENAME__', target='calendar', target_sortorder=1)
           ]


