import pytest
from mklists import ListLine

def test_hardbroken_line():
    x = ListLine('http://example.org\n')
    output = """http://example.org <br>\n"""
    assert x.hardbroken_line() == output

def test_hardbroken_line_already_br():
    x = ListLine('http://example.org <br>\n')
    output = """http://example.org <br>\n"""
    assert x.hardbroken_line() == output

