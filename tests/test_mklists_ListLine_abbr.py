import pytest
import mklists
from mklists import ListLine

def test_addbr():
    x = ListLine('http://example.org\n')
    output = """http://example.org <br>\n"""
    assert x.addbr().line == output

def test_addbr_already_br():
    x = ListLine('http://example.org <br>\n')
    output = """http://example.org <br>\n"""
    assert x.addbr().line == output

