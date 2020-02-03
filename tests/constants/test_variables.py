"""@@@Docstring"""


from mklists.constants import (
    CONFIG_YAMLFILE_NAME,
    ROOTDIR_RULEFILE_NAME,
    DATADIR_RULEFILE_NAME,
)


def test_defaults_config_yamlfile_name():
    """@@@Docstring"""
    assert CONFIG_YAMLFILE_NAME == "mklists.yml"
    assert ROOTDIR_RULEFILE_NAME == "rules.cfg"
    assert DATADIR_RULEFILE_NAME == ".rules"
