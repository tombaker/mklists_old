"""Return YAML string given a Python data object."""

import os
import pytest
from mklists.utils import return_yamlstr_from_dataobj, return_yamlobj_from_yamlstr

RESULT_YAMLSTR = r"""verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}
"""


def test_utils_return_yamlstr_from_dataobj():
    """Return YAML string given a Python data object.
    Round-trip the conversion because dictionary order
    is arbitrary."""
    dataobj = {
        "verbose": False,
        "html_yes": False,
        "backup_depth_int": 3,
        "invalid_filename_patterns": ["\\.swp$", "\\.tmp$", "~$", "^\\."],
        "files2dirs_dict": {},
    }
    assert return_yamlobj_from_yamlstr(return_yamlstr_from_dataobj(dataobj)) == dataobj
