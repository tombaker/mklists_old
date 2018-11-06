"""Utility module"""

import os
import re
import glob
from mklists import (
    URL_PATTERN_REGEX,
    INVALID_FILENAME_PATS,
    VALID_FILENAME_CHARS_STR,
    DatadirNotAccessibleError,
    BadFileFormatError,
)


def change_working_directory(dirname, verb=False):
    """Set current working directory for mklists (data)."""
    if dirname is not None:
        try:
            os.chdir(dirname)
            if verb:
                print(f"Changing to {repr(dirname)} as working directory.")
        except FileNotFoundError:
            raise DatadirNotAccessibleError(f"{dirname} is not accessible.")


def is_file(object_path):
    """Returns True if object is a file."""
    if not os.path.isfile(object_path):
        return False
    return True


def has_valid_name(
    file_name,
    bad_patterns=INVALID_FILENAME_PATS,
    valid_chars=VALID_FILENAME_CHARS_STR,
):
    """Return True if filename has no invalid characters or patterns.

    Used to stop execution of mklists if data folder has files that
    should not be processed, such as temporary or backup files.
    """
    for bad_pattern in bad_patterns:
        if re.search(bad_pattern, file_name):
            print(
                f"Bad pattern {repr(bad_pattern)} "
                f"in filename {repr(file_name)}."
            )
            return False
    for char in file_name:
        if char not in valid_chars:
            print(f"{repr(char)} is not a valid filename character.")
            return False
    return True


def has_valid_contents(filename):
    """Returns True if file is UTF8-encoded and has no blank lines.

    Raises:
        BadFileFormatError: if file is not UTF8-encoded.

    TODO Does not tell user whether it is failing because
    * not UTF8
    * has blank lines
    """
    try:
        with open(filename) as chk_for_blank_lines:
            for line in chk_for_blank_lines:
                if not line.rstrip():
                    return False
    except UnicodeDecodeError:
        raise BadFileFormatError(f"{repr(filename)} is not in UTF-8 format.")
    return True


def _is_utf8_encoded(file_name):
    """Returns True if file is UTF8-encoded.

    Raises:
        BadFileFormatError: if file is not UTF8-encoded.
    """
    try:
        open(file_name).read()
    except UnicodeDecodeError:
        raise BadFileFormatError(f"{repr(file_name)} is not in UTF-8 format.")
    return True


def _has_no_blank_lines(text_file):
    """Returns True if file has no blank lines.

    Note: Does not test whether text_file is a text file."""
    with open(text_file) as fin:
        for line in fin:
            if not line.rstrip():
                return False
    return True


def linkify(string_raw):
    """docstring"""
    if "<a href=" in string_raw:
        return string_raw
    return re.compile(URL_PATTERN_REGEX).sub(
        r'<a href="\1">\1</a>', string_raw
    )


def ls_visible(cwd=os.getcwd()):
    """Do I need to break this out into separate function?"""
    os.chdir(cwd)
    return [name for name in glob.glob("*")]
