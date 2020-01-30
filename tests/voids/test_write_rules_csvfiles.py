"""Write default starter rule files."""

import os
from pathlib import Path
from mklists.constants import (
    RULEFILE_NAME,
    DATADIRA_RULEFILE_CONTENTS,
    DATADIRA_NAME,
    ROOTDIR_RULEFILE_CONTENTS,
    ROOTDIR_RULEFILE_NAME,
)
from mklists.voids import write_rules_csvfiles


def test_init_write_rules_csvfiles(tmp_path):
    """Write global rulefile in root, starter rulefile in data directory."""
    os.chdir(tmp_path)
    root_rules = Path(ROOTDIR_RULEFILE_NAME)
    root_rules_contents = ROOTDIR_RULEFILE_CONTENTS
    datadira_rules = Path(DATADIRA_NAME) / RULEFILE_NAME
    datadira_rules_contents = DATADIRA_RULEFILE_CONTENTS
    write_rules_csvfiles()
    assert Path(root_rules).read_text() == root_rules_contents
    assert Path(datadira_rules).read_text() == datadira_rules_contents
