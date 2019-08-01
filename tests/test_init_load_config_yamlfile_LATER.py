"""@@@"""

# import io
# import os
# import pytest
# from mklists.initialize import (
#     CONFIG_YAMLFILE_NAME,
#     MINIMAL_CONFIG_YAMLFILE_STR,
#     load_config_yamlfile,
#     write_initial_config_yamlfile,
# )


# def test_init_load_config_yamlfile(tmpdir):
#     """See /Users/tbaker/github/tombaker/mklists/mklists/initialize.py"""
#     os.chdir(tmpdir)
#     write_initial_config_yamlfile()
#     assert load_config_yamlfile() == yaml.load(open(CONFIG_YAMLFILE_NAME).read())
#
#
# def test_init_load_config_yamlfile_notfound(tmpdir):
#     """See /Users/tbaker/github/tombaker/mklists/mklists/initialize.py"""
#     os.chdir(tmpdir)
#     with pytest.raises(FileNotFoundError):
#         load_config_yamlfile()
