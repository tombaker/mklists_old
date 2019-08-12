"""Test utils.py - _return_htmlstr_from_textstr"""

from mklists.utils import _return_htmlstr_from_textstr


def test_utils_return_htmlstr_from_textstr_linkified_line_already_linkified():
    """@@@Docstring"""
    putin = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    putout = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line():
    """@@@Docstring"""
    putin = """http://example.org"""
    putout = """<a href="http://example.org">http://example.org</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_non_url():
    """Shows that function does not test for non-sensical URLs."""
    putin = """http://..."""
    putout = """<a href="http://...">http://...</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_question_mark():
    """@@@Docstring"""
    putin = """http://192.168.2.1/html/login/status.html?lang=en"""
    putout = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_ip_address():
    """@@@Docstring"""
    putin = """http://192.168.56.100:8888/"""
    putout = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_3d():
    """@@@Docstring"""
    putin = """http://carnegieeurope.eu/strategiceurope/?fa=3D64063="""
    putout = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_hashsign():
    """@@@Docstring"""
    putin = """http://ctrlpvim.github.io/ctrlp.vim/#installation"""
    putout = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_colon():
    """@@@Docstring"""
    putin = """http://en.wikipedia.org/wiki/Talk:Dublin_Core"""
    putout = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_escaped_characters():
    """@@@Docstring"""
    putin = """http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29"""
    putout = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_colon2():
    """@@@Docstring"""
    putin = """http://explore.dublincore.net/rdf/lrmi/#/resource"""
    putout = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_bang():
    """@@@Docstring"""
    putin = """http://twitter.com/#!/search/%23dcmi11"""
    putout = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_comma():
    """This application will not accept commas as valid URL characters."""
    putin = """http://standorte.deutschepost.de,"""
    putout = """<a href="http://standorte.deutschepost.de">http://standorte.deutschepost.de</a>,"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_url_with_https():
    """@@@Docstring"""
    putin = """https://www.w3.org/2013/data/CG/wiki"""
    putout = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_surrounded_by_brackets():
    """@@@Docstring"""
    putin = """see info (https://www.w3.org/2013/data/CG/wiki)'"""
    putout = """see info (<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>)'"""
    assert _return_htmlstr_from_textstr(putin) == putout


def test_utils_return_htmlstr_from_textstr_linkified_line_with_two_urls():
    """@@@Docstring"""
    putin = """see info (https://example1.org), http://example2.org)"""
    putout = """see info (<a href="https://example1.org">https://example1.org</a>), <a href="http://example2.org">http://example2.org</a>)"""
    assert _return_htmlstr_from_textstr(putin) == putout
