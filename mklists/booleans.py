"""Boolean functions."""

import re
from pathlib import Path
from .constants import VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError, MissingValueError

# pylint: disable=bad-continuation
#         Black disagrees.


def filename_is_valid_as_filename(
    filename=None,
    invalid_filename_patterns=None,
    valid_filename_characters_regex=VALID_FILENAME_CHARACTERS_REGEX,
):
    """Return True if filename:
    * is not None
    * does not match "invalid filename" regex
    * does not match name of an existing directory in current directory"""
    if filename is None:
        raise MissingValueError(f"Missing filename.")
    if invalid_filename_patterns:
        for badpat in invalid_filename_patterns:
            if re.search(badpat, filename):
                return False
    for char in filename:
        if not bool(re.search(valid_filename_characters_regex, char)):
            return False
    if Path(filename).is_dir():
        raise FilenameIsAlreadyDirnameError(f"{repr(filename)} is already a directory.")
    return True


def dataline_is_match_to_ruleobj(ruleobj=None, dataline_str=None):
    """Returns True if data line matches pattern specified in given rule."""
    # Line does not match if given field greater than number of fields in line.
    if ruleobj.source_matchfield > len(dataline_str.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if ruleobj.source_matchfield == 0:
        if re.search(ruleobj.source_matchpattern, dataline_str):
            return True

    # Line matches if pattern is found in given field.
    if ruleobj.source_matchfield > 0:
        eth = ruleobj.source_matchfield - 1
        if re.search(ruleobj.source_matchpattern, dataline_str.split()[eth]):
            return True

    return False


def regex_is_valid_as_regex(regex=None):
    """@@@Docstring"""
    try:
        re.compile(regex)
    except re.error:
        return False
    return True
