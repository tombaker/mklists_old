from mklists.rule import *


def test_rulestring():
    input = '0  /./         lines         __RENAME__   0'
    output = ['0', '.', 'lines', '__RENAME__', '0']
    assert parse_rulestring(input) == output

def test_rulestring_regex_has_space():
    input = '0  /^= 20/     __RENAME__    calendar     1 # regex has a space'
    output = ['0', '^= 20', '__RENAME__', 'calendar', '1']
    assert parse_rulestring(input) == output

def test_rulestring_not_enough_fields():
    input = '1  /TRACK/     __RENAME__    '
    output = ['1', 'TRACK', '__RENAME__']
    assert parse_rulestring(input) == output

def test_rulestring_field1_is_not_digit():
    input = 'x  /FTMP/      __RENAME__    a            0'
    output = ['x', 'FTMP', '__RENAME__', 'a', '0']
    assert parse_rulestring(input) == output

def test_rulestring_is_empty():
    input = ''
    output = []
    assert parse_rulestring(input) == output

def test_rulestring_is_comment_only():
    input = '# blank lines and lines that start with hash get ignored'
    output = ['# blank lines and lines that start with hash get ignored']
    assert parse_rulestring(input) == output

