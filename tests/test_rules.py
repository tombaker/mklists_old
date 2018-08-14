import pytest
from mklists.rules import *

@pytest.mark.skip
def test_source_is_registered():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    Rule.register(x)
    y = Rule('1', 'LATER', 'b.txt', 'c.txt', '0')
    assert Rule.register(y)

@pytest.mark.skip
def test_source_is_registered_not():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    Rule.register(x)
    y = Rule('1', 'LATER', 'c.txt', 'd.txt', '0')
    with pytest.raises(SystemExit):
        Rule.register(y)

@pytest.mark.rule
def test_validate_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    y = Rule(1, '.', 'a', 'b', 2)
    assert x.validate() == y

@pytest.mark.rule
def test_validate_rule_not():
    x = Rule('1', 'N(OW', 'a', 'b', '2')
    with pytest.raises(SystemExit):
        x.validate()

@pytest.mark.rule
def test_rule():
    x = Rule('1', '.', 'a', 'b', '2')
    assert x.source == 'a'

@pytest.mark.rule
def test_rulestring_regex_has_space():
    x = Rule('1', '^X 19', 'a', 'b', '2')
    assert x.source_matchpattern == '^X 19'

@pytest.mark.rule
def test_source_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._source_filename_valid()

@pytest.mark.rule
def test_target_filename_valid():
    x = Rule('1', '^X 19', 'a.txt', 'b.txt', '2')
    assert x._target_filename_valid()

@pytest.mark.rule
def test_target_filename_valid_not():
    x = Rule('1', '^X 19', 'a.txt', 'b^.txt', '2')
    with pytest.raises(SystemExit):
        x._target_filename_valid()

@pytest.mark.rule
def test_source_matchfield_is_integer():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_matchfield_is_integer

@pytest.mark.rule
def test_target_sortorder_is_integer():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._target_sortorder_is_integer

@pytest.mark.rule
def test_source_ne_target():
    x = Rule('1', 'NOW', 'a.txt', 'b.txt', '0')
    assert x._source_not_equal_target

@pytest.mark.rule
def test_source_ne_target_not():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_not_equal_target()

@pytest.mark.rule
def test_source_matchpattern_is_valid():
    x = Rule('1', 'NOW', 'a.txt', 'a.txt', '0')
    assert x._source_matchpattern_is_valid

@pytest.mark.rule
def test_source_matchpattern_is_valid_not():
    x = Rule('1', 'N(OW', 'a.txt', 'a.txt', '0')
    with pytest.raises(SystemExit):
        x._source_matchpattern_is_valid()

# def test_rulestring():
#     input = '0  /./         lines         __RENAME__   0'
#     output = ['0', '.', 'lines', '__RENAME__', '0']
#     assert srule_to_lrule(input) == output
# 
# def test_rulestring_regex_has_space():
#     input = '0  /^= 20/     __RENAME__    calendar     1 # regex has a space'
#     output = ['0', '^= 20', '__RENAME__', 'calendar', '1']
#     assert srule_to_lrule(input) == output
# 
# def test_rulestring_not_enough_fields():
#     input = '1  /TRACK/     __RENAME__    '
#     output = ['1', 'TRACK', '__RENAME__']
#     assert srule_to_lrule(input) == output
# 
# def test_rulestring_field1_is_not_digit():
#     input = 'x  /FTMP/      __RENAME__    a            0'
#     output = ['x', 'FTMP', '__RENAME__', 'a', '0']
#     assert srule_to_lrule(input) == output
# 
# def test_rulestring_is_empty():
#     input = ''
#     output = []
#     assert srule_to_lrule(input) == output
# 
# def test_rulestring_is_comment_only():
#     input = '# blank lines and lines that start with hash get ignored'
#     output = []
#     assert srule_to_lrule(input) == output
# 
# def test_srules_to_lrules():
#     input = [ 
#              '0  /./         lines         __RENAME__   0',
#              '0  /^= 20/     __RENAME__    calendar     1 # regex has a space',
#              '1  /TRACK/     __RENAME__    ',
#              'x  /FTMP/      __RENAME__    a            0',
#              '',
#              '# blank lines and lines that start with hash get ignored'
#             ]
#     output = [['0', '.', 'lines', '__RENAME__', '0'],
#               ['0', '^= 20', '__RENAME__', 'calendar', '1'],
#               ['1', 'TRACK', '__RENAME__'],
#               ['x', 'FTMP', '__RENAME__', 'a', '0']]
#     assert srules_to_lrules(input) == output
# 
# def test_check_lrule_field1_error_exit():
#     input = [['x', 'FTMP', '__RENAME__', 'a', '0']]
#     with pytest.raises(SystemExit):
#         check_lrules(input)
# 
# def test_lrule_backto_srule():
#     input = [0, '\/n', 'a.txt', 'b.txt', 0]
#     output = '0 /\/n/ a.txt b.txt 0'
#     assert lrule_backto_srule(input) == output
# 
# def test_lrule_backto_srule_one_field_only():
#     input = [0]
#     output = '0'
#     assert lrule_backto_srule(input) == output

#    Usage:
#        x = RulestringParser
#        x.get_stringrules('_rules', '_rules_correct')
#        x.parse_stringrules_to_splitrules()
#        x.splitrules_to_ruleobjects()
#        x.validate_rules()
