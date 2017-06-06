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

def test_md2html_url_with_question_mark():
    input_string = """http://192.168.2.1/html/login/status.html?lang=en"""
    output_markdown = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_ip_address():
    input_string = """http://192.168.56.100:8888/"""
    output_markdown = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_3D():
    input_string = """http://carnegieeurope.eu/strategiceurope/?fa=3D64063="""
    output_markdown = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_hashsign():
    input_string = """http://ctrlpvim.github.io/ctrlp.vim/#installation"""
    output_markdown = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_colon():
    input_string = """http://en.wikipedia.org/wiki/Talk:Dublin_Core"""
    output_markdown = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_escaped_characters():
    input_string = """http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29"""
    output_markdown = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_colon2():
    input_string = """http://explore.dublincore.net/rdf/lrmi/#/resource"""
    output_markdown = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_bang():
    input_string = """http://twitter.com/#!/search/%23dcmi11"""
    output_markdown = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_comma():
    input_string = """http://standorte.deutschepost.de,"""
    output_markdown = """<a href="http://standorte.deutschepost.de,">http://standorte.deutschepost.de,</a>"""
    assert mklists.md2html(input_string) == output_markdown

def test_md2html_url_with_doublequotemark():
    """Edge case of extraneous double-quote mark."""
    input_string = 'http://www..."'
    output_markdown = 'http://www..."'
    assert mklists.md2html(input_string) != output_markdown

def test_md2html_url_with_https():
    input_string = """https://www.w3.org/2013/data/CG/wiki"""
    output_markdown = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
    assert mklists.md2html(input_string) == output_markdown

