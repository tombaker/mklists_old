"""Tests for todo.py"""

import os
import pytest
from mklists.utils import return_htmlline_str_from_textstr

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

# NOTUSE> DATADICT_AFTER = {
# NOTUSE>     "dcmi.txt": [
# NOTUSE>         "DC2019 "
# NOTUSE>         '<a href="http://dublincore.org/conferences/2019">'
# NOTUSE>         "http://dublincore.org/conferences/2019</a>\n",
# NOTUSE>         "DC2019 Sep 23-26\n",
# NOTUSE>     ],
# NOTUSE>     "shex.txt": [
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


@pytest.mark.skip
def test_write_htmlfiles_from_datadict(tmpdir):
    """@@@Docstring"""
    tmpdira = tmpdir.mkdir("a")
    os.chdir(tmpdira)
    datadir_pathname = tmpdira
    rootdir_pathname = tmpdir
    htmldir_pathname = os.path.join(rootdir_pathname, ".html", "a")
    filename2datalines_dict = DATADICT_BEFORE
    files_to_be_created = []
    lines_to_be_printed = []
    for key in list(filename2datalines_dict.keys()):
        files_to_be_created.append(os.path.join(htmldir_pathname, key))
        for line in filename2datalines_dict[key]:
            lines_to_be_printed.append(return_htmlline_str_from_textstr(line))
    print(files_to_be_created)
    print(lines_to_be_printed)
    # 2019-08-17: Pick up here.
    assert False
