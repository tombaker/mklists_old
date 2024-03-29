"""Wraps URLs found in text lines with HTML tags to make them clickable."""

from mklists.returns import linkify_textline


def test_linkify_textline_linkified_line_already_linkified():
    """Line already containing HREF tags are left untouched."""
    textline = """Line with <a href="http://example.org">http://example.org</a>.\n"""
    htmlline = """Line with <a href="http://example.org">http://example.org</a>.\n"""
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line():
    """@@@Docstring"""
    textline = """http://example.org"""
    htmlline = """<a href="http://example.org">http://example.org</a>\n"""
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_non_url():
    """Shows that function does not test for non-sensical URLs."""
    textline = """http://..."""
    htmlline = """<a href="http://...">http://...</a>\n"""
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_question_mark():
    """@@@Docstring"""
    textline = """http://192.168.2.1/x.html?lang=en"""
    htmlline = (
        """<a href="http://192.168.2.1/x.html?la"""
        """ng=en">http://192.168.2.1/x.html?lang=en</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_ip_address():
    """@@@Docstring"""
    textline = """http://192.168.56.100:8888/"""
    htmlline = (
        """<a href="http://192.168.56.100:8888/">"""
        """http://192.168.56.100:8888/</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_3d():
    """@@@Docstring"""
    textline = """http://foo.eu/?fa=3D64063="""
    htmlline = (
        """<a href="http://foo.eu/?fa=3D64063=">"""
        """http://foo.eu/?fa=3D64063=</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_hashsign():
    """@@@Docstring"""
    textline = """http://bar.github.io/#inst"""
    htmlline = (
        """<a href="http://bar.github.io/#inst">http://bar.github.io/#inst</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_url_with_colon():
    """@@@Docstring"""
    textline = """http://foobar.org/Talk:Xyz"""
    htmlline = (
        """<a href="http://foobar.org/Talk:Xyz">http://foobar.org/Talk:Xyz</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_url_with_escaped_characters():
    """@@@Docstring"""
    # pylint: disable=line-too-long
    # Regrettably, yes.
    textline = """http://ex.org/Rizzi_%28DE-537%29"""
    htmlline = (
        """<a href="http://ex.org/Rizzi_%28"""
        """DE-537%29">http://ex.org/Rizzi_%28DE-537%29</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_colon2():
    """@@@Docstring"""
    textline = """http://ex.net/rdf/lrmi/#/res"""
    htmlline = (
        """<a href="http://ex.net/rdf/lrmi/#/res">http://ex.net/rdf/lrmi/#/res</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_bang():
    """@@@Docstring"""
    # pylint: disable=line-too-long
    # Regrettably, yes.
    textline = """http://ex.com/#!/search/%23dcmi11"""
    htmlline = (
        """<a href="http://ex.com/#!/search/%23dcm"""
        """i11">http://ex.com/#!/search/%23dcmi11</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_comma():
    """This application will not accept commas as valid URL characters."""
    # pylint: disable=line-too-long
    # Regrettably, yes.
    textline = """http://standorte.deutschepost.de,"""
    htmlline = (
        """<a href="http://standorte.deutsche"""
        """post.de">http://standorte.deutschepost.de</a>,\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_url_with_https():
    """@@@Docstring"""
    textline = """https://www.w3.org/wiki"""
    htmlline = """<a href="https://www.w3.org/wiki">https://www.w3.org/wiki</a>\n"""
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_surrounded_by_brackets():
    """Note the single apostrophone."""
    textline = """see info (https://www.w3.org/wiki)'"""
    htmlline = (
        """see info (<a href="https://www.w3.or"""
        """g/wiki">https://www.w3.org/wiki</a>)'\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_linkified_line_with_two_urls():
    """@@@Docstring"""
    textline = """(https://1) http://2"""
    htmlline = (
        """(<a href="https://1">https://1</a>) <a href="http://2">http://2</a>\n"""
    )
    assert linkify_textline(textline) == htmlline


def test_linkify_textline_not_including_linefeed():
    """@@@Docstring"""
    textline = """http://www.gmd.de\n"""
    htmlline = """<a href="http://www.gmd.de">http://www.gmd.de</a>\n"""
    assert linkify_textline(textline) == htmlline
