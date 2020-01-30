"""@@@Docstring"""


from mklists.constants import (
    CONFIG_YAMLFILE_NAME,
    HTMLDIR_NAME,
    ROOTDIR_RULEFILE_NAME,
    RULEFILE_NAME,
)


def test_defaults_config_yamlfile_name():
    """@@@Docstring"""
    assert CONFIG_YAMLFILE_NAME == "mklists.yml"
    assert HTMLDIR_NAME == "_html"
    assert ROOTDIR_RULEFILE_NAME == "rules.cfg"
    assert RULEFILE_NAME == ".rules"
