"""Boolean functions."""


import os
import re
import pytest
from .constants import INVALID_FILENAME_REGEXES, VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError


@pytest.mark.improve
def line_is_match_to_rule(_given_ruleobj=None, _given_dataline_str=None):
    """Returns True if data line matches pattern specified in given rule."""

    # if is_valid_as_regex(_given_ruleobj
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


def is_valid_as_filename(
    _file_tobetested_name=None,
    _datadir_pathname=None,
    _invalid_filename_regexes_list=INVALID_FILENAME_REGEXES,
    _valid_filename_characters_regex_str=VALID_FILENAME_CHARACTERS_REGEX,
):
    """Return True if filename:
    * has no invalid characters (override defaults in mklists.yml)
    * string patterns (override defaults in mklists.yml)
    * does not match name of an existing directory in current directory

    @@@ 2018-08-12
    Maybe this should _not_ take _invalid_filename_regexes_list and
    _valid_filename_characters_regex_str as arguments but should read
    them from the context object.
    """
    if not _datadir_pathname:
        _datadir_pathname = os.getcwd()
    for badpat in _invalid_filename_regexes_list:
        if re.search(badpat, _file_tobetested_name):
            return False
    for char in _file_tobetested_name:
        if not bool(re.search(_valid_filename_characters_regex_str, char)):
            return False
    if _file_tobetested_name in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(
            f"Filename {repr(_file_tobetested_name)} is already used as a directory name."
        )
    return True


def is_valid_as_regex(_regex=None):
    """@@@Docstring"""
    try:
        re.compile(_regex)
    except re.error:
        return False
    return True
