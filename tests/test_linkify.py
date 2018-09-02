import pytest
from mklists.utils import linkify


def test_linkified_line_already_linkified():
    input = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    output = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    assert linkify(input) == output


def test_linkified_line():
    input = """http://example.org"""
    output = """<a href="http://example.org">http://example.org</a>"""
    assert linkify(input) == output


def test_linkified_line_non_url():
    """Shows that function does not test for non-sensical URLs."""
    input = """http://..."""
    output = """<a href="http://...">http://...</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_question_mark():
    input = """http://192.168.2.1/html/login/status.html?lang=en"""
    output = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_ip_address():
    input = """http://192.168.56.100:8888/"""
    output = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_3D():
    input = """http://carnegieeurope.eu/strategiceurope/?fa=3D64063="""
    output = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_hashsign():
    input = """http://ctrlpvim.github.io/ctrlp.vim/#installation"""
    output = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_colon():
    input = """http://en.wikipedia.org/wiki/Talk:Dublin_Core"""
    output = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_escaped_characters():
    input = """http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29"""
    output = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_colon2():
    input = """http://explore.dublincore.net/rdf/lrmi/#/resource"""
    output = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_bang():
    input = """http://twitter.com/#!/search/%23dcmi11"""
    output = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
    assert linkify(input) == output


def test_linkified_line_url_with_comma():
    """This application will not accept commas as valid URL characters."""
    input = """http://standorte.deutschepost.de,"""
    output = """<a href="http://standorte.deutschepost.de">http://standorte.deutschepost.de</a>,"""
    assert linkify(input) == output


def test_linkified_line_url_with_https():
    input = """https://www.w3.org/2013/data/CG/wiki"""
    output = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
    assert linkify(input) == output


@pytest.mark.skip
def test_linkified_line_surrounded_by_brackets():
    input = """see info (https://www.w3.org/2013/data/CG/wiki)"""
    output = """see info (<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>)')"""

@pytest.mark.skip
def test_linkified_line_with_two_urls():
    input = """see info (https://example1.org), http://example2.org"""
    output = """see info (<a href="https://example1.org">https://example1.org</a>), <a href="http://example2.org">http://example2.org</a>)"""
