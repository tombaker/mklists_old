import pytest
import mklists
from mklists import ListLine

def test_linkify_already_urlified():
    x = ListLine('A line with <a href="http://example.org">http://example.org</a>.\n')
    output = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    assert x.linkify().line == output

def test_linkify():
    x = ListLine('http://example.org')
    output = """<a href="http://example.org">http://example.org</a>"""
    assert x.linkify().line == output

def test_linkify_non_url():
    """Shows that function does not test for non-sensical URLs."""
    x = ListLine('http://...')
    output = """<a href="http://...">http://...</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_question_mark():
    x = ListLine('http://192.168.2.1/html/login/status.html?lang=en')
    output = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_ip_address():
    x = ListLine('http://192.168.56.100:8888/')
    output = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_3D():
    x = ListLine('http://carnegieeurope.eu/strategiceurope/?fa=3D64063=')
    output = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_hashsign():
    x = ListLine('http://ctrlpvim.github.io/ctrlp.vim/#installation')
    output = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_colon():
    x = ListLine('http://en.wikipedia.org/wiki/Talk:Dublin_Core')
    output = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_escaped_characters():
    x = ListLine('http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29')
    output = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_colon2():
    x = ListLine('http://explore.dublincore.net/rdf/lrmi/#/resource')
    output = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_bang():
    x = ListLine('http://twitter.com/#!/search/%23dcmi11')
    output = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_comma():
    x = ListLine('http://standorte.deutschepost.de,')
    output = """<a href="http://standorte.deutschepost.de,">http://standorte.deutschepost.de,</a>"""
    assert x.linkify().line == output

def test_linkify_url_with_doublequotemark():
    """
    Edge case of extraneous double-quote mark.
    """
    x = ListLine('http://www..."')
    output = 'http://www..."'
    assert x.linkify().line != output

def test_linkify_url_with_https():
    x = ListLine('https://www.w3.org/2013/data/CG/wiki')
    output = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
    assert x.linkify().line == output

