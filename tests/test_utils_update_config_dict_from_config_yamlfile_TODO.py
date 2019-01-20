"""@@@Docstring"""

from mklists.utils import update_config_dict_from_config_yamlfile


def test_update_config_dict_from_config_yamlfile():
    """Updates original settings with new unless value was originally None."""
    initial = {"verbose": True}
    overrides = {"backups": 1, "html": True, "verbose": None}
    result_dict = {"verbose": True, "backups": 1, "html": True}
    assert update_config_dict_from_config_yamlfile(initial, overrides) == result_dict


def test_update_config_dict_from_config_yamlfile2():
    """Updates original settings with new unless value was originally None."""
    initial = {"ctx": "something", "backups": 1}
    overrides = {"backups": 500}
    expected = {"ctx": "something", "backups": 500}
    assert update_config_dict_from_config_yamlfile(initial, overrides) == expected
