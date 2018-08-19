import pytest
import yaml
from textwrap import dedent
from mklists.rule import Rule

@pytest.fixture(scope='module')
def rule_global_yaml(tmpdir_factory):
    """Write some YAML-formatted rules to YAML rule files."""

    yaml_rule_data = """\
    - [0,  '.'        , lines        , __RENAME__   , 0]
    - [0,  '^= 20'    , __RENAME__   , calendar     , 1]
    """

    rules = tmpdir_factory.mktemp('datadir').join('rules')
    print(f"Created 'rules': {repr(rules)}")
    rules.write(dedent(yaml_rule_data))

    return rules

@pytest.fixture(scope='module')
def rule_yaml(tmpdir_factory):
    """Write some YAML-formatted rules to YAML rule files."""

    yaml_rule_data = """\
    - [0   , 'NOW'    , lines        , __RENAME__   , 0]
    - [0   , 'LATER'  , __RENAME__   , calendar     , 1]
    """

    rules = tmpdir_factory.mktemp('datadir').join('rules')
    print(f"Created 'rules': {repr(rules)}")
    rules.write(dedent(yaml_rule_data))

    return rules

@pytest.fixture(scope='module')
def rules_python():
    return [
                Rule(source_matchfield=0, source_matchpattern='.', source='lines', target='__RENAME__', target_sortorder=0),
                Rule(source_matchfield=0, source_matchpattern='^= 20', source='__RENAME__', target='calendar', target_sortorder=1),
                Rule(source_matchfield=0, source_matchpattern='NOW', source='lines', target='__RENAME__', target_sortorder=0),
                Rule(source_matchfield=0, source_matchpattern='LATER', source='__RENAME__', target='calendar', target_sortorder=1)
           ]







#rules = [['0', 'i', 'a.txt', 'b.txt', '0']]
#lines = ['two ticks\n', 'an ant\n', 'the mite\n']
#output = {'a.txt': ['an ant\n'], 'b.txt': ['two ticks\n', 'the mite\n']}

#rules = [['2', 'i', 'a.txt', 'b.txt', '1']]
#lines = ['two ticks\n', 'an ant\n', 'the mite\n']
#output = {'a.txt': ['an ant\n'], 'b.txt': ['the mite\n', 'two ticks\n']}
