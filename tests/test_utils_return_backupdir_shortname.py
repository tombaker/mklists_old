"""@@@Docstring"""

import pytest
from mklists.config import Defaults

fixed = Defaults()

# @pytest.mark.skip
# def test_backups_return_backupdir_shortname():
#     """@@@Docstring"""
#     root_dir = "/Users/tbaker/foobar"
#     list_dir = "/Users/tbaker/foobar/agenda"
#     expected = "agenda"
#     assert (
#         return_backupdir_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
#         == expected
#     )
#
#
# @pytest.mark.skip
# def test_backups_return_backupdir_shortname_two_deep():
#     """@@@Docstring"""
#     root_dir = "/Users/tbaker/foobar"
#     list_dir = "/Users/tbaker/foobar/a/b"
#     expected = "a_b"
#     assert (
#         return_backupdir_shortname(rootdir_pathname=root_dir, datadir_pathname=list_dir)
#         == expected
#     )
