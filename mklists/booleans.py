"""Boolean functions."""


import os
import re
import pytest

# from .constants import INVALID_FILENAME_REGEXES, VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError, MissingValueError


def filename_is_valid_as_filename(
    _filename=None,
    _invalid_filename_regexes_list=None,
    _valid_filename_characters_regex_str=None,
):
    """Return True if filename:
    * is not None
    * has no invalid characters (override defaults in mklists.yml)
    * string patterns (override defaults in mklists.yml)
    * does not match name of an existing directory in current directory
    """
    if _filename is None:
        raise MissingValueError(f"Missing filename.")
    for badpat in _invalid_filename_regexes_list:
        if re.search(badpat, _filename):
            return False
    for char in _filename:
        if not bool(re.search(_valid_filename_characters_regex_str, char)):
            return False
    if _filename in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(f"{repr(_filename)} is a directory.")
    return True


@pytest.mark.improve
def dataline_is_match_to_ruleobj(_given_ruleobj=None, _given_dataline_str=None):
    """Returns True if data line matches pattern specified in given rule.

    2019-09-28: This function assumes that the rule object received
    is valid, its validity having been tested by
    run/return_ruleobj_list_from_rulefile_pathname_chain()."""

    # if regex_is_valid_as_regex(_given_ruleobj
    # @@@TODO

    # Line does not match if given field greater than number of fields in line.
    if _given_ruleobj.source_matchfield > len(_given_dataline_str.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if _given_ruleobj.source_matchfield == 0:
        if re.search(_given_ruleobj.source_matchpattern, _given_dataline_str):
            return True

    # Line matches if pattern is found in given field.
    if _given_ruleobj.source_matchfield > 0:
        eth = _given_ruleobj.source_matchfield - 1
        if re.search(
            _given_ruleobj.source_matchpattern, _given_dataline_str.split()[eth]
        ):
            return True

    return False


def regex_is_valid_as_regex(_regex=None):
    """@@@Docstring"""
    try:
        re.compile(_regex)
    except re.error:
        return False
    return True
