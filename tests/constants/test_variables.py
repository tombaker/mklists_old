"""@@@Docstring"""


from mklists.constants import CONFIG_YAMLFILE_NAME, HTMLDIR_NAME, RULES_CSVFILE_NAME


def test_defaults_config_yamlfile_name():
    """@@@Docstring"""
    assert CONFIG_YAMLFILE_NAME == "mklists.yml"
    assert HTMLDIR_NAME == "html"
    assert RULES_CSVFILE_NAME == ".rules"
