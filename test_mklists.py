import pytest
import mklists

def test_md2html():
    input_string = """http://example.org"""
    output_markdown = """<a href="http://example.org">http://example.org</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_non_url():
    """Shows that function does not test against non-sensical URLs."""
    input_string = """http://..."""
    output_markdown = """<a href="http://...">http://...</a>"""
    assert mklists.md2html(input_string) == output_markdown

# http://....
# http://192.168.2.1/html/login/status.html?lang=en
# http://192.168.56.100:8888/
# http://carnegieeurope.eu/strategiceurope/?fa=3D64063=
# http://ctrlpvim.github.io/ctrlp.vim/#installation
# http://www.w3.org/News/2012#entry-9470
# http://en.wikipedia.org/wiki/Talk:Dublin_Core
# http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29
# http://explore.dublincore.net/rdf/lrmi/#/resource
# http://standorte.deutschepost.de,
# http://twitter.com/#!/search/%23dcmi11
# http://www..."
# http://www.w3.org/Consortium/application?key=861d49f272d5318c203c3e911accd0ba
# https://www.w3.org/2013/data/CG/wiki/Telecon:2014.11.19
