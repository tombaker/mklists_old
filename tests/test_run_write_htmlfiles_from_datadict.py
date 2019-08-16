"""Tests for todo.py"""

import pytest

DATADICT_BEFORE = {
    "dcmi.txt": [
        "DC2019 http://dublincore.org/conferences/2019\n",
        "DC2019 Sep 23-26\n",
    ],
    "shex.txt": [
        "SHEX Primer: http://shex.io/shex-primer\n",
        "SHEX Wikidata: http://bit.ly/shex_in_wikidata\n",
    ],
}

DATADICT_AFTER = {
    "dcmi.txt": [
        "DC2019 "
        '<a href="http://dublincore.org/conferences/2019">'
        "http://dublincore.org/conferences/2019</a>\n",
        "DC2019 Sep 23-26\n",
    ],
    "shex.txt": [
        "SHEX Primer: "
        '<a href="http://shex.io/shex-primer">'
        "http://shex.io/shex-primer</a>\n",
        "SHEX Wikidata: "
        '<a href="http://bit.ly/shex_in_wikidata">'
        "http://bit.ly/shex_in_wikidata</a>\n",
    ],
}

DCMI_HTML_FILE_STR = """\
DC2019 <a href="http://dublincore.org/conferences/2019">http://dublincore.org/conferences/2019</a>
DC2019 Sep 23-26
"""

SHEX_HTML_FILE_STR = """\
SHEX Primer: <a href="http://shex.io/shex-primer">http://shex.io/shex-primer</a>
SHEX Wikidata: <a href="http://bit.ly/shex_in_wikidata">http://bit.ly/shex_in_wikidata</a>
"""


@pytest.mark.skip(reason="todo")
def test_write_htmlfiles_from_datadict():
    """@@@Docstring"""
    assert False
