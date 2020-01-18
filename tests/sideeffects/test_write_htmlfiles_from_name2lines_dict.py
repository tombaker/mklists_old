"""Tests for todo.py"""

import io
import os
import pytest
from mklists.sideeffects import write_htmlfiles_from_name2lines_dict
from mklists.utils import return_htmlline_from_textline, return_visiblefiles_list

DATADICT_BEFORE = {
    "filea.txt": [
        "DC2019 http://dublincore.org/conferences/2019\n",
        "DC2019 Sep 23-26\n",
    ],
    "fileb.txt": [
        "SHEX Primer: http://shex.io/shex-primer\n",
        "SHEX Wikidata: http://bit.ly/shex_in_wikidata\n",
    ],
}

TEST_FILEA_HTMLSTR = """\
DC2019 <a href="http://dublincore.org/conferences/2019">http://dublincore.org/conferences/2019</a>
DC2019 Sep 23-26
"""

TEST_FILEB_HTMLSTR = """\
SHEX Primer: <a href="http://shex.io/shex-primer">http://shex.io/shex-primer</a>
SHEX Wikidata: <a href="http://bit.ly/shex_in_wikidata">http://bit.ly/shex_in_wikidata</a>
"""


def test_write_htmlfiles_from_name2lines_dict(tmpdir):
    """Writes datalines to HTML files in HTML directory."""
    htmldir_subdir_pathname = os.path.join(tmpdir, ".html", "a")
    os.makedirs(htmldir_subdir_pathname, exist_ok=True)
    os.chdir(htmldir_subdir_pathname)
    write_htmlfiles_from_name2lines_dict(
        name2lines_dict=DATADICT_BEFORE,
        htmldir_pathname=os.path.join(tmpdir, ".html"),
        backupdir_shortname="a",
    )
    assert io.open("filea.txt.html").read() == TEST_FILEA_HTMLSTR
    assert io.open("fileb.txt.html").read() == TEST_FILEB_HTMLSTR


def test_write_htmlfiles_from_name2lines_dict_first_deletes_existing_files(tmpdir):
    """Deletes existing files in HTML directory before writing datalines."""
    htmldir_subdir_pathname = os.path.join(tmpdir, ".html", "a")
    os.makedirs(htmldir_subdir_pathname, exist_ok=True)
    os.chdir(htmldir_subdir_pathname)
    io.open("some_file.txt.html", mode="w", encoding="utf-8").write("some content")
    write_htmlfiles_from_name2lines_dict(
        name2lines_dict=DATADICT_BEFORE,
        htmldir_pathname=os.path.join(tmpdir, ".html"),
        backupdir_shortname="a",
    )
    assert io.open("filea.txt.html").read() == TEST_FILEA_HTMLSTR
    assert io.open("fileb.txt.html").read() == TEST_FILEB_HTMLSTR
    assert not os.path.exists("some_file.txt.html")
