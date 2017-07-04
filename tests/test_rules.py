import pytest
from rules import RuleLine

def test_rule_line():
    input = '1 . source.txt target.txt 3\n'
    x = RuleLine(input)
    output = """http://example.org <br>\n"""
    assert x.line == input

def test_rule_line_strip_comments():
    input = '1 . source.txt target.txt 3 # This is a comment\n'
    x = RuleLine(input)
    output = '1 . source.txt target.txt 3'
    assert x.line == output
