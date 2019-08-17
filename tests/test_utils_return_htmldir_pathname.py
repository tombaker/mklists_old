"""Returns pathname of HTML directory, composed from info provided in arguments.

Edit /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import os
import pytest
from mklists.constants import HTMLDIR_NAME
from mklists.utils import return_htmldir_pathname


def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory."""
    rootdir_pathname = "/Users/tbaker/tmp"
    htmldir_name = ".html"
    currentdir_pathname = "agenda"
    expected = "/Users/tbaker/tmp/.html/agenda"
    assert (
        return_htmldir_pathname(
            _rootdir_pathname=rootdir_pathname,
            _htmldir_name=htmldir_name,
            _currentdir_pathname=currentdir_pathname,
        )
        == expected
    )


def test_utils_return_htmldir_pathname_rootdir_pathname_not_given():
    """Returns pathname of HTML directory."""
    htmldir_name = ".html"
    currentdir_pathname = "agenda"
    with pytest.raises(SystemExit):
        return_htmldir_pathname(
            _rootdir_pathname=None,
            _htmldir_name=htmldir_name,
            _currentdir_pathname=currentdir_pathname,
        )


def test_utils_return_htmldir_pathname_htmldir_name_not_given():
    """Raises exception if argument _htmldir_name not provided."""
    rootdir_pathname = "/Users/tbaker/tmp"
    currentdir_pathname = "agenda"
    expected = "/Users/tbaker/tmp/.html/agenda"  # uses value of HTMLDIR_NAME
    assert (
        return_htmldir_pathname(
            _rootdir_pathname=rootdir_pathname, _currentdir_pathname=currentdir_pathname
        )
        == expected
    )


def test_utils_return_htmldir_pathname_current_pathname_not_given(tmpdir):
    """Returns pathname of HTML directory."""
    os.chdir(tmpdir)
    rootdir_pathname = "/Users/tbaker/tmp"
    htmldir_name = ".html"
    currentdir_pathname = str(tmpdir)
    assert currentdir_pathname in return_htmldir_pathname(
        _rootdir_pathname=rootdir_pathname,
        _htmldir_name=htmldir_name,
        _currentdir_pathname=None,
    )
