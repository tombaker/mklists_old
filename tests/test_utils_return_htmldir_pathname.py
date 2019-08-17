"""Returns pathname of HTML directory, composed from info provided in arguments.

Edit /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""

import pytest
from mklists.utils import return_htmldir_pathname


@pytest.mark.skip
def test_utils_return_htmldir_pathname():
    """Returns pathname of HTML directory where
    all needed info is provided in arguments.

    Args:
        _rootdir_pathname:
        _htmldir_name:
        _currentdir_pathname:
    """
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
