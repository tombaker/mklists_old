"""Constructs pathname of root-level '_html' directory."""

import os
import pytest
from pathlib import Path
from mklists.returns import get_htmldir_path

HTMLDIR_NAME = "_html"


def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory."""
    rd = "/Users/tbaker/tmp"
    hd = "_html"
    dd = "/Users/tbaker/tmp/agenda"
    expected = Path("/Users/tbaker/tmp/_html/agenda")
    assert get_htmldir_path(rootdir=rd, htmldir=hd, datadir=dd) == expected


def test_utils_return_htmldir_pathname_html_subdirectories_nested():
    """Structure of HTML directory mirrors structure of data directories."""
    rd = "/Users/tbaker/tmp"
    hd = "_html"
    dd = "/Users/tbaker/tmp/a/b"
    expected = Path("/Users/tbaker/tmp/_html/a/b")
    real = get_htmldir_path(rootdir=rd, htmldir=hd, datadir=dd)
    assert real == expected


@pytest.mark.skip
def test_utils_return_htmldir_pathname_rootdir_pathname_not_given():
    """Raises exception if argument root not provided."""
    hd = "_html"
    dd = "agenda"
    with pytest.raises(SystemExit):
        get_htmldir_path(rootdir=None, htmldir=hd, datadir=dd)


@pytest.mark.skip
def test_utils_return_htmldir_pathname_htmldir_name_not_given(tmp_path):
    """Raises exception if HTML directory name is deliberately omitted."""
    os.chdir(tmp_path)
    with pytest.raises(SystemExit):
        get_htmldir_path(htmldir=None)


@pytest.mark.skip
def test_utils_return_htmldir_pathname_datadir_name_not_given(tmp_path):
    """Returns pathname of HTML directory."""
    os.chdir(tmp_path)
    Path("mklists.yml").write_text("config stuff")
    # pylint: disable=unused-variable
    # Yes, by design.
    dirname, datadir = os.path.split(os.getcwd())
    os.chdir(tmp_path)
    expected = Path(tmp_path).joinpath(datadir)
    assert get_htmldir_path(datadir=datadir) == expected
