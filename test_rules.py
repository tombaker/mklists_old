import pytest
from rules import RuleLine

def test_rule_line():
    input = '1 . source.txt target.txt 3\n'
    x = RuleLine(input)
    output = """http://example.org <br>\n"""
    assert x.line == input

