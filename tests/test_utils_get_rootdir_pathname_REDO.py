"""Return repo root pathname when executed anywhere within repo.

    Look for mandatory file CONFIG_YAMLFILE_NAME ('mklists.yml').

    Starting at PWD, should look for:
    * file 'mklists.yml' - and if found, return full pathname
    * root directory - and if found, exit with error message

See /Users/tbaker/github/tombaker/mklists/mklists/utils.py
"""


# import os
# import pytest
# from mklists.initialize import CONFIG_YAMLFILE_NAME
# from mklists.utils import get_rootdir_pathname


# def test_get_rootdir_pathname_from_fixture_subdir(myrepo):
#     """Find root pathname for fixture "myrepo"."""
#     os.chdir(os.path.join(myrepo, "a"))
#     assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname())
#
#
# def test_get_rootdir_pathname_while_in_rootdir(tmpdir):
#     """Find root directory while in root directory."""
#     tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
#     os.chdir(tmpdir)
#     assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname())
#
#
# def test_get_rootdir_pathname_while_in_subdir_one_deep(tmpdir):
#     """Find root directory while in subdir one deep."""
#     tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
#     tmpdira = tmpdir.mkdir("a")
#     tmpdira.join(RULE_YAMLFILE_NAME).write("some rules")
#     os.chdir(tmpdira)
#     assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname())
#
#
# def test_get_rootdir_pathname_while_in_subdir_two_deep(tmpdir):
#     """Find root directory while in subdir two deep."""
#     tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
#     tmpdira = tmpdir.mkdir("a")
#     tmpdirb = tmpdira.mkdir("b")
#     os.chdir(tmpdirb)
#     assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname())
#
#
# def test_get_rootdir_pathname_while_in_subdir_three_deep(tmpdir):
#     """Find root directory while in subdir three deep."""
#     tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
#     tmpdira = tmpdir.mkdir("a")
#     tmpdirb = tmpdira.mkdir("b")
#     tmpdirc = tmpdirb.mkdir("c")
#     os.chdir(tmpdirc)
#     assert CONFIG_YAMLFILE_NAME in os.listdir(get_rootdir_pathname())
#
#
# def test_not_get_rootdir_pathname_given_missing_link(tmpdir):
#     """Do not find root directory when rulefile chain has missing link."""
#     tmpdir.join(CONFIG_YAMLFILE_NAME).write("config stuff")
#     tmpdira = tmpdir.mkdir("a")
#     tmpdirb = tmpdira.mkdir("b")
#     tmpdirb.join("foobar").write("some more rules")
#     tmpdirc = tmpdirb.mkdir("c")
#     os.chdir(tmpdirc)
#     with pytest.raises(SystemExit):
#         get_rootdir_pathname()
