"""@@@Docstring"""

from mklists.utils import update_settings_dict


def test_update_settings_dict():
    """Updates original settings with new unless value was originally None."""
    starter_dict = {"verbose": True}
    override_dict = {"backups": 1, "html": True, "verbose": None}
    result_dict = {"verbose": True, "backups": 1, "html": True}
    assert update_settings_dict(starter_dict, override_dict) == result_dict


def test_update_settings_dict2():
    """Updates original settings with new unless value was originally None."""
    initial_context = {"ctx": "something", "backups": 1}
    overrides_from_file = {"backups": 500}
    expected = {"ctx": "something", "backups": 500}
    assert update_settings_dict(initial_context, overrides_from_file) == expected
