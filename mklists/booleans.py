"""Boolean functions."""


import os
import re
from .constants import INVALID_FILENAME_PATTERNS, VALID_FILENAME_CHARACTERS_REGEX
from .exceptions import FilenameIsAlreadyDirnameError


def is_valid_as_filename(
    filename=None,
    current_dir=None,
    badpats=INVALID_FILENAME_PATTERNS,
    validchars_regex=VALID_FILENAME_CHARACTERS_REGEX,
):
    """Return True if filename:
    * has no invalid characters (override defaults in mklists.yml)
    * string patterns (override defaults in mklists.yml)
    * does not match name of an existing directory in current_dir

    """
    if not current_dir:
        current_dir = os.getcwd()
    for badpat in badpats:
        if re.search(badpat, filename):
            return False
    for char in filename:
        if not bool(re.search(validchars_regex, char)):
            return False
    if filename in [d for d in os.listdir() if os.path.isdir(d)]:
        raise FilenameIsAlreadyDirnameError(
            f"Filename {repr(filename)} is already used as a directory name."
        )
    return True


def is_line_match_to_rule(given_rule=None, given_line=None):
    """Returns True if data line matches pattern specified in given rule."""

    # Line does not match if given field greater than number of fields in line.
    if given_rule.source_matchfield > len(given_line.split()):
        return False

    # Line matches if given field is zero and pattern found anywhere in line.
    if given_rule.source_matchfield == 0:
        if re.search(given_rule.source_matchpattern, given_line):
            return True

    # Line matches if pattern is found in given field.
    if given_rule.source_matchfield > 0:
        eth = given_rule.source_matchfield - 1
        if re.search(given_rule.source_matchpattern, given_line.split()[eth]):
            return True

    return False
