"""
Here: /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile.py
"""

import io
import os
from mklists.initialize import (
    CONFIG_YAMLFILE_NAME,
    CONFIG_YAMLFILE_STR,
    write_config_yamlfile,
)


def test_init_write_config_yamlfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_config_yamlfile(
        _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
        _file_tobewritten_str=CONFIG_YAMLFILE_STR,
    )
    assert io.open(CONFIG_YAMLFILE_NAME).read() == CONFIG_YAMLFILE_STR


# test_init_write_initial_rule_yamlfiles.py
# test_init_write_newbie_datafiles.py
# test_init_write_newbie_rule_yamlfiles.py
# test_run_write_datadict_to_datafiles_in_currentdir.py
# test_run_write_htmlfiles_from_datadict.py
# TIMESTAMP_STR
# INVALID_FILENAME_REGEXES
# URL_PATTERN_REGEX
# VALID_FILENAME_CHARACTERS_REGEX
# BACKUPDIR_NAME
# HTMLDIR_NAME
# CONFIG_YAMLFILE_NAME
# RULE_YAMLFILE_NAME
# CONFIG_YAMLFILE_STR
# MINIMAL_DATADIRA_RULES_YAMLFILE_STR
# CONFIG_YAMLFILE_STR
# ROOTDIR_RULES_YAMLSTR
# EXAMPLE_DATADIRA_RULES_YAMLSTR
# EXAMPLE_DATADIRB_RULES_YAMLSTR
