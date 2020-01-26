"""Write default starter rule files."""

import os
from pathlib import Path
from mklists.constants import (
    RULES_CSVFILE_NAME,
    DATADIRA_RULES_CSVFILE_CONTENTS,
    DATADIRA_NAME,
    ROOTDIR_RULES_CSVFILE_CONTENTS,
)
from mklists.voids import write_rules_csvfiles


def test_init_write_rules_csvfiles(tmp_path):
    """Write global rulefile in root, starter rulefile in data directory."""
    os.chdir(tmp_path)
    root_rules = Path(RULES_CSVFILE_NAME)
    datadira_rules = Path(DATADIRA_NAME) / RULES_CSVFILE_NAME
    root_rules_contents = ROOTDIR_RULES_CSVFILE_CONTENTS
    datadira_rules_contents = DATADIRA_RULES_CSVFILE_CONTENTS
    write_rules_csvfiles()
    assert Path(root_rules).read_text() == root_rules_contents
    assert Path(datadira_rules).read_text() == datadira_rules_contents
