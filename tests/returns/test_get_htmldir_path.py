"""Constructs pathname of root-level '_html' directory."""

import os
import pytest
from pathlib import Path
from mklists.returns import get_htmldir_path

HTMLDIR_NAME = "_html"


def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory."""
    rd = "/Users/tbaker/tmp"
    hd = HTMLDIR_NAME
    dd = "/Users/tbaker/tmp/agenda"
    expected = Path("/Users/tbaker/tmp").joinpath(HTMLDIR_NAME, "agenda")
    assert get_htmldir_path(rootdir=rd, htmldir=hd, datadir=dd) == expected


def test_utils_return_htmldir_pathname_html_subdirectories_nested():
    """Structure of HTML directory mirrors structure of data directories."""
    rd = "/Users/tbaker/tmp"
    dd = "/Users/tbaker/tmp/a/b"
    expected = Path("/Users/tbaker/tmp").joinpath(HTMLDIR_NAME, "a/b")
    real = get_htmldir_path(rootdir=rd, datadir=dd)
    assert real == expected


def test_utils_return_htmldir_pathname_rootdir_pathname_not_given(tmp_path):
    """Raises exception if argument root not provided."""
    os.chdir(tmp_path)
    dd = "agenda"
    with pytest.raises(SystemExit):
        get_htmldir_path(rootdir=None, datadir=dd)


def test_utils_return_htmldir_pathname_htmldir_name_not_given(tmp_path):
    """Raises exception if HTML directory name is deliberately omitted."""
    os.chdir(tmp_path)
    with pytest.raises(SystemExit):
        get_htmldir_path(htmldir=None)


def test_utils_return_htmldir_pathname_datadir_name_not_given(tmp_path):
    """Returns pathname of HTML directory."""
    Path(tmp_path).joinpath("mklists.yml").write_text("config stuff")
    ab = Path(tmp_path).joinpath("a/b")
    ab.mkdir(parents=True, exist_ok=True)
    os.chdir(ab)
    assert HTMLDIR_NAME == "_html"
    expected = Path(tmp_path) / HTMLDIR_NAME / "a/b"
    assert get_htmldir_path() == expected
