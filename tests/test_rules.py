import pytest
from mklists.rules import *


def test_rulestring():
    input = '0  /./         lines         __RENAME__   0'
    output = ['0', '.', 'lines', '__RENAME__', '0']
    assert stringrule_to_listrule(input) == output

def test_rulestring_regex_has_space():
    input = '0  /^= 20/     __RENAME__    calendar     1 # regex has a space'
    output = ['0', '^= 20', '__RENAME__', 'calendar', '1']
    assert stringrule_to_listrule(input) == output

def test_rulestring_not_enough_fields():
    input = '1  /TRACK/     __RENAME__    '
    output = ['1', 'TRACK', '__RENAME__']
    assert stringrule_to_listrule(input) == output

def test_rulestring_field1_is_not_digit():
    input = 'x  /FTMP/      __RENAME__    a            0'
    output = ['x', 'FTMP', '__RENAME__', 'a', '0']
    assert stringrule_to_listrule(input) == output

def test_rulestring_is_empty():
    input = ''
    output = []
    assert stringrule_to_listrule(input) == output

def test_rulestring_is_comment_only():
    input = '# blank lines and lines that start with hash get ignored'
    output = []
    assert stringrule_to_listrule(input) == output

def test_stringrules_to_listrules():
    input = [ 
             '0  /./         lines         __RENAME__   0',
             '0  /^= 20/     __RENAME__    calendar     1 # regex has a space',
             '1  /TRACK/     __RENAME__    ',
             'x  /FTMP/      __RENAME__    a            0',
             '',
             '# blank lines and lines that start with hash get ignored'
            ]
    output = [['0', '.', 'lines', '__RENAME__', '0'],
              ['0', '^= 20', '__RENAME__', 'calendar', '1'],
              ['1', 'TRACK', '__RENAME__'],
              ['x', 'FTMP', '__RENAME__', 'a', '0']]
    assert stringrules_to_listrules(input) == output

def test_check_listrule_field1_error_exit():
    input = [['x', 'FTMP', '__RENAME__', 'a', '0']]
    with pytest.raises(SystemExit):
        check_listrules(input)

def test_listrule_backto_stringrule():
    input = [0, '\/n', 'a.txt', 'b.txt', 0]
    output = '0 /\/n/ a.txt b.txt 0'
    assert listrule_backto_stringrule(input) == output

def test_listrule_backto_stringrule_one_field_only():
    input = [0]
    output = '0'
    assert listrule_backto_stringrule(input) == output

