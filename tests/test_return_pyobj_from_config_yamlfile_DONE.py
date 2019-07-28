"""@@@Docstring"""

import yaml
from mklists.utils import return_pyobj_from_config_yamlfile


def test_write_yamlstr_to_yamlfile(tmpdir):
    yaml_str = "backups: 3\nverbose: false"
    yamlfile = "mklists.yml"
    with open(yamlfile, "w") as fout:
        fout.write(yaml_str)
    result = {"backups": 3, "verbose": False}
    assert return_pyobj_from_config_yamlfile(yamlfile) == result


def test_write_yamlstr_to_yamlfile_too(tmpdir):
    """Writes string to YAML rulefile, reads it back to string."""
    lr_yamlstr = """
    - [1, 'NOW', a, b, 0]
    - [1, 'LATER', a, c, 0]"""
    with open("_rules", "w") as fout:
        fout.write(lr_yamlstr)
    assert lr_yamlstr == open("_rules").read()
