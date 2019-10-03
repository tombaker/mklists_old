"""Test utils.py - return_htmlline_from_textline"""

import pytest
from mklists.utils import return_htmlline_from_textline


def test_utils_return_htmlline_from_textline_linkified_line_already_linkified():
    """@@@Docstring"""
    putin = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    putout = """A line with <a href="http://example.org">http://example.org</a>.\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line():
    """@@@Docstring"""
    putin = """http://example.org"""
    putout = """<a href="http://example.org">http://example.org</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_non_url():
    """Shows that function does not test for non-sensical URLs."""
    putin = """http://..."""
    putout = """<a href="http://...">http://...</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_question_mark():
    """@@@Docstring"""
    putin = """http://192.168.2.1/x.html?lang=en"""
    putout = """<a href="http://192.168.2.1/x.html?lang=en">http://192.168.2.1/x.html?lang=en</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_ip_address():
    """@@@Docstring"""
    putin = """http://192.168.56.100:8888/"""
    putout = (
        """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>\n"""
    )
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_3d():
    """@@@Docstring"""
    putin = """http://foo.eu/?fa=3D64063="""
    putout = """<a href="http://foo.eu/?fa=3D64063=">http://foo.eu/?fa=3D64063=</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_hashsign():
    """@@@Docstring"""
    putin = """http://bar.github.io/#inst"""
    putout = """<a href="http://bar.github.io/#inst">http://bar.github.io/#inst</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_colon():
    """@@@Docstring"""
    putin = """http://foobar.org/Talk:Xyz"""
    putout = """<a href="http://foobar.org/Talk:Xyz">http://foobar.org/Talk:Xyz</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_escaped_characters():
    """@@@Docstring"""
    putin = """http://ex.org/Rizzi_%28DE-537%29"""
    putout = """<a href="http://ex.org/Rizzi_%28DE-537%29">http://ex.org/Rizzi_%28DE-537%29</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_colon2():
    """@@@Docstring"""
    putin = """http://ex.net/rdf/lrmi/#/res"""
    putout = (
        """<a href="http://ex.net/rdf/lrmi/#/res">http://ex.net/rdf/lrmi/#/res</a>\n"""
    )
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_bang():
    """@@@Docstring"""
    putin = """http://ex.com/#!/search/%23dcmi11"""
    putout = """<a href="http://ex.com/#!/search/%23dcmi11">http://ex.com/#!/search/%23dcmi11</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_comma():
    """This application will not accept commas as valid URL characters."""
    putin = """http://standorte.deutschepost.de,"""
    putout = """<a href="http://standorte.deutschepost.de">http://standorte.deutschepost.de</a>,\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_url_with_https():
    """@@@Docstring"""
    putin = """https://www.w3.org/wiki"""
    putout = """<a href="https://www.w3.org/wiki">https://www.w3.org/wiki</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_surrounded_by_brackets():
    """Note the single apostrophone."""
    putin = """see info (https://www.w3.org/wiki)'"""
    putout = """see info (<a href="https://www.w3.org/wiki">https://www.w3.org/wiki</a>)'\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_linkified_line_with_two_urls():
    """@@@Docstring"""
    putin = """(https://1) http://2"""
    putout = """(<a href="https://1">https://1</a>) <a href="http://2">http://2</a>\n"""
    assert return_htmlline_from_textline(putin) == putout


@pytest.mark.skip
def test_utils_return_htmlline_from_textline_not_including_linefeed():
    """@@@Docstring"""
    putin = """http://www.gmd.de\n"""
    putout = """<a href="http://www.gmd.de">http://www.gmd.de</a>\n"""
    print(type(putout))
    print(putout)
    assert return_htmlline_from_textline(putin) == putout
