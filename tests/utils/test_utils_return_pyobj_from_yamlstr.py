"""Return YAML string given a Python data object."""

import os
import pytest
from mklists.utils import return_yamlstr_from_pyobj, return_pyobj_from_yamlstr

YMLSTR = """verbose: True
htmlify: True
backup_depth: 3
invalid_filename_patterns:
- \.swp$
- \.tmp$
- ~$
- ^\.

# For given file, destination directory to which it should be moved
files2dirs:
    to_a.txt: a
    to_b.txt: b
    to_c.txt: /Users/foo/logs"""

PYOBJ = {
    "verbose": True,
    "htmlify": True,
    "backup_depth": 3,
    "invalid_filename_patterns": ["\\.swp$", "\\.tmp$", "~$", "^\\."],
    "files2dirs": {"to_a.txt": "a", "to_b.txt": "b", "to_c.txt": "/Users/foo/logs"},
}


def test_utils_return_yamlstr_from_pyobj():
    """Return Python data object from a given YAML string."""
    assert return_pyobj_from_yamlstr(YMLSTR) == PYOBJ
