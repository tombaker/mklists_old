"""Boolean functions."""


import os
import re
from .constants import VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError, MissingValueError

# pylint: disable=bad-continuation
#         Black disagrees.


def filename_is_valid_as_filename(filename, invalid_filename_patterns=None):
    """Return True if filename:
    * is not None
    * does not match an "invalid filename" regex
    * does not match name of an existing directory in current directory
    """
    if filename is None:
        raise MissingValueError(f"Missing filename.")
    if invalid_filename_patterns:
        for badpat in invalid_filename_patterns:
            if re.search(badpat, filename):
                return False
    for char in filename:
        if not bool(re.search(VALID_FILENAME_CHARACTERS_REGEX, char)):
            return False
    if filename in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(f"{repr(filename)} is a directory.")
    return True


def dataline_is_match_to_ruleobj(given_ruleobj=None, given_dataline_str=None):
    """Returns True if data line matches pattern specified in given rule.

    2019-09-28: This function assumes that the rule object received
    is valid, its validity having been tested by
    run/return_ruleobj_list_from_rulefile_pathname_chain()."""

    # Line does not match if given field greater than number of fields in line.
    if given_ruleobj.source_matchfield > len(given_dataline_str.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_ruleobj.source_matchfield == 0:
        if re.search(given_ruleobj.source_matchpattern, given_dataline_str):
            return True

    # Line matches if pattern is found in given field.
    if given_ruleobj.source_matchfield > 0:
        eth = given_ruleobj.source_matchfield - 1
        if re.search(
            given_ruleobj.source_matchpattern, given_dataline_str.split()[eth]
        ):
            return True

    return False


def regex_is_valid_as_regex(regex=None):
    """@@@Docstring"""
    try:
        re.compile(regex)
    except re.error:
        return False
    return True
