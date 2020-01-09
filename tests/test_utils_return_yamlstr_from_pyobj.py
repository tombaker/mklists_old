"""Return YAML string given a Python data object."""

import os
import pytest
from mklists.utils import return_yamlstr_from_pyobj, return_pyobj_from_yamlstr

RESULT_YAMLSTR = r"""verbose: false
htmlify: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}
"""


def test_utils_return_yamlstr_from_pyobj():
    """Return YAML string given a Python data object.
    Round-trip the conversion because dictionary order
    is arbitrary."""
    pyobj = {
        "verbose": False,
        "htmlify": False,
        "backup_depth_int": 3,
        "invalid_filename_patterns": ["\\.swp$", "\\.tmp$", "~$", "^\\."],
        "files2dirs_dict": {},
    }
    assert return_pyobj_from_yamlstr(return_yamlstr_from_pyobj(pyobj)) == pyobj
