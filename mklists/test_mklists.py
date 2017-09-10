import pytest
from collections import namedtuple

Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')

# test mklists.mustbetext()
from mklists import istext

def test_istext():
    with pytest.raises(SystemExit):
        istext('_non-text.png')

# test mklists.shuffle()
from mklists import shuffle

def test_shuffle():
    rules_l1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 0) ]
    globlines_l1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['two ticks\n', 'the mite\n'] }
    assert shuffle(rules_l1, globlines_l1) == output

def test_shuffle_sort():
    rules_l1 = [ Rule(2, 'i', 'a.txt', 'b.txt', 1) ]
    globlines_l1 = ['two ticks\n', 'an ant\n', 'the mite\n']
    output = { 'a.txt': ['an ant\n'], 'b.txt': ['the mite\n', 'two ticks\n'] }
    assert shuffle(rules_l1, globlines_l1) == output

# # test mklists.RuleLine
# from mklists import RuleLine
# 
# def test_rule_line_strip_comments():
#     x = RuleLine('1 . source.txt target.txt 3 # This is a comment\n')
#     output = '1 . source.txt target.txt 3'
#     assert x.line.strip_comments() == output

# test mklists.ListLine
from mklists import ListLine

def test_linkified_line_already_linkified():
    x = ListLine('A line with <a href="http://example.org">http://example.org</a>.\n')
    output_line = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    assert x.linkified_line() == output_line

def test_linkified_line():
    x = ListLine('http://example.org')
    output_line = """<a href="http://example.org">http://example.org</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_non_url():
    """Shows that function does not test for non-sensical URLs."""
    x = ListLine('http://...')
    output_line = """<a href="http://...">http://...</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_question_mark():
    x = ListLine('http://192.168.2.1/html/login/status.html?lang=en')
    output_line = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_ip_address():
    x = ListLine('http://192.168.56.100:8888/')
    output_line = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_3D():
    x = ListLine('http://carnegieeurope.eu/strategiceurope/?fa=3D64063=')
    output_line = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_hashsign():
    x = ListLine('http://ctrlpvim.github.io/ctrlp.vim/#installation')
    output_line = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_colon():
    x = ListLine('http://en.wikipedia.org/wiki/Talk:Dublin_Core')
    output_line = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_escaped_characters():
    x = ListLine('http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29')
    output_line = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_colon2():
    x = ListLine('http://explore.dublincore.net/rdf/lrmi/#/resource')
    output_line = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_bang():
    x = ListLine('http://twitter.com/#!/search/%23dcmi11')
    output_line = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_comma():
    """This application will not accept commas as valid URL characters."""
    x = ListLine('http://standorte.deutschepost.de,')
    output_line = """<a href="http://standorte.deutschepost.de">http://standorte.deutschepost.de</a>,"""
    assert x.linkified_line() == output_line

def test_linkified_line_url_with_https():
    x = ListLine('https://www.w3.org/2013/data/CG/wiki')
    output_line = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
    assert x.linkified_line() == output_line

def test_linkified_line_surrounded_by_brackets():
    x = ListLine('see info (https://www.w3.org/2013/data/CG/wiki)')
    output_line = """see info (<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>)')"""

def test_linkified_line_with_two_urls():
    x = ListLine('see info (https://example1.org), http://example2.org')
    output_line = """see info (<a href="https://example1.org">https://example1.org</a>), <a href="http://example2.org">http://example2.org</a>)"""
