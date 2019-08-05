"""Boolean functions."""


import os
import re
from .constants import INVALID_FILENAME_REGEXES, VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError


def is_valid_as_filename(
    _file_tested_name=None,
    _current_dirname=None,
    _invalid_filename_regexes=INVALID_FILENAME_REGEXES,
    validchars_regex=VALID_FILENAME_CHARACTERS_REGEX,
):
    """Return True if filename:
    * has no invalid characters (override defaults in mklists.yml)
    * string patterns (override defaults in mklists.yml)
    * does not match name of an existing directory in current directory

    """
    if not _current_dirname:
        _current_dirname = os.getcwd()
    for badpat in _invalid_filename_regexes:
        if re.search(badpat, _file_tested_name):
            return False
    for char in _file_tested_name:
        if not bool(re.search(validchars_regex, char)):
            return False
    if _file_tested_name in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(
            f"Filename {repr(_file_tested_name)} is already used as a directory name."
        )
    return True


def is_line_match_to_rule(_given_ruleobj=None, _given_datafile_line=None):
    """Returns True if data line matches pattern specified in given rule."""

    # Line does not match if given field greater than number of fields in line.
    if _given_ruleobj.source_matchfield > len(_given_datafile_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if _given_ruleobj.source_matchfield == 0:
        if re.search(_given_ruleobj.source_matchpattern, _given_datafile_line):
            return True

    # Line matches if pattern is found in given field.
    if _given_ruleobj.source_matchfield > 0:
        eth = _given_ruleobj.source_matchfield - 1
        if re.search(
            _given_ruleobj.source_matchpattern, _given_datafile_line.split()[eth]
        ):
            return True

    return False
