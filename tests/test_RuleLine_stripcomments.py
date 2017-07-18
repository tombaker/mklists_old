import pytest
from rules import RuleLine

def test_rule_line_strip_comments():
    x = RuleLine('1 . source.txt target.txt 3 # This is a comment\n')
    output = '1 . source.txt target.txt 3'
    assert x.line.strip_comments() == output
