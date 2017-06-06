import pytest
import mklists

def test_md2html():
    input_string = """http://example.org"""
    output_markdown = """<a href="http://example.org">http://example.org</a>"""
    assert mklists.md2html(input_string) == output_markdown

