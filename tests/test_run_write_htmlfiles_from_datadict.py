"""Tests for todo.py"""

import io
import os
import pytest
from mklists.run import write_htmlfiles_from_datadict
from mklists.utils import return_htmlline_str_from_textstr

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

# NOTUSE> DATADICT_AFTER = {
# NOTUSE>     "filea.txt": [
# NOTUSE>         "DC2019 "
# NOTUSE>         '<a href="http://dublincore.org/conferences/2019">'
# NOTUSE>         "http://dublincore.org/conferences/2019</a>\n",
# NOTUSE>         "DC2019 Sep 23-26\n",
# NOTUSE>     ],
# NOTUSE>     "fileb.txt": [
# NOTUSE>         "SHEX Primer: "
# NOTUSE>         '<a href="http://shex.io/shex-primer">'
# NOTUSE>         "http://shex.io/shex-primer</a>\n",
# NOTUSE>         "SHEX Wikidata: "
# NOTUSE>         '<a href="http://bit.ly/shex_in_wikidata">'
# NOTUSE>         "http://bit.ly/shex_in_wikidata</a>\n",
# NOTUSE>     ],
# NOTUSE> }

TEST_FILEA_HTMLSTR = """\
DC2019 <a href="http://dublincore.org/conferences/2019">http://dublincore.org/conferences/2019</a>
DC2019 Sep 23-26
"""

TEST_FILEB_HTMLSTR = """\
SHEX Primer: <a href="http://shex.io/shex-primer">http://shex.io/shex-primer</a>
SHEX Wikidata: <a href="http://bit.ly/shex_in_wikidata">http://bit.ly/shex_in_wikidata</a>
"""


def test_write_htmlfiles_from_datadict(tmpdir):
    """Writes datalines to HTML files in HTML directory."""
    htmldir_subdir_pathname = os.path.join(tmpdir, ".html", "a")
    os.makedirs(htmldir_subdir_pathname, exist_ok=True)
    os.chdir(htmldir_subdir_pathname)
    write_htmlfiles_from_datadict(
        _filename2datalines_dict=DATADICT_BEFORE,
        _htmldir_pathname=os.path.join(tmpdir, ".html"),
        _backupdir_shortname="a",
    )
    assert io.open("filea.txt.html").read() == TEST_FILEA_HTMLSTR
    assert io.open("fileb.txt.html").read() == TEST_FILEB_HTMLSTR


def test_write_htmlfiles_from_datadict_first_deletes_existing_files(tmpdir):
    """Deletes existing files in HTML directory before writing datalines."""
    htmldir_subdir_pathname = os.path.join(tmpdir, ".html", "a")
    os.makedirs(htmldir_subdir_pathname, exist_ok=True)
    os.chdir(htmldir_subdir_pathname)
    htmldir_subdir_pathname.join("some_file.txt.html").write("some content")
    write_htmlfiles_from_datadict(
        _filename2datalines_dict=DATADICT_BEFORE,
        _htmldir_pathname=os.path.join(tmpdir, ".html"),
        _backupdir_shortname="a",
    )
    assert io.open("filea.txt.html").read() == TEST_FILEA_HTMLSTR
    assert io.open("fileb.txt.html").read() == TEST_FILEB_HTMLSTR
