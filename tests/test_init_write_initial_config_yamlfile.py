"""
Here: /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile.py
"""

import io
import os
from mklists.initialize import (
    CONFIG_YAMLFILE_NAME,
    MINIMAL_CONFIG_YAMLFILE_STR,
    write_minimal_config_yamlfile,
)


def test_init_write_minimal_config_yamlfile(tmpdir):
    """@@@Docstring"""
    os.chdir(tmpdir)
    write_minimal_config_yamlfile(
        _file_tobewritten_name=CONFIG_YAMLFILE_NAME,
        _file_tobewritten_str=MINIMAL_CONFIG_YAMLFILE_STR,
    )
    assert io.open(CONFIG_YAMLFILE_NAME).read() == MINIMAL_CONFIG_YAMLFILE_STR


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
# MINIMAL_CONFIG_YAMLFILE_STR
# MINIMAL_ADIR_RULES_YAMLFILE_STR
# NEWBIE_CONFIG_YAMLFILE_STR
# NEWBIE_ROOTDIR_RULES_YAMLSTR
# NEWBIE_DATADIRA_RULES_YAMLSTR
# NEWBIE_DATADIRB_RULES_YAMLSTR
