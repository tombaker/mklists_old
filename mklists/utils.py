"""Utility module"""

import os
import re
import glob
from mklists import (
    URL_PATTERN,
    INVALID_FILENAME_PATS,
    VALID_FILENAME_CHARS,
    DatadirNotAccessibleError,
    DatadirHasNonFilesError,
    BadFileFormatError,
    BadFilenameError,
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
    """Returns True if object is a file.

    Raises:
        DatadirHasNonFilesError: if object is not a file.
    """

    if not os.path.isfile(object_path):
        return False
    return True


def has_valid_name(
    filename,
    bad_patterns=INVALID_FILENAME_PATS,
    valid_chars=VALID_FILENAME_CHARS,
):
    """Return True if filename has no invalid characters or patterns.

    Used to block execution of mklists if the data
    folder has any files that should not be processed,
    such as temporary files or backup files.

    Raises:
        BadFilenameError: if filename matches a bad pattern.
    """
    for bad_pattern in bad_patterns:
        if re.search(bad_pattern, filename):
            print(
                f"Bad pattern {repr(bad_pattern)} "
                f"in filename {repr(filename)}."
            )
            return False
    for char in filename:
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
        with open(filename) as tf:
            for line in tf:
                if not line.rstrip():
                    return False
    except UnicodeDecodeError:
        raise BadFileFormatError(f"{repr(filename)} is not in UTF-8 format.")
    return True


def _is_utf8_encoded(file):
    """Returns True if a data files is UTF8-encoded.

    Raises:
        BadFileFormatError: if any file is not UTF8-encoded.
    """
    try:
        open(file).read()
    except UnicodeDecodeError:
        raise BadFileFormatError(f"{repr(filename)} is not in UTF-8 format.")
    return True


def _has_no_blank_lines(text_file):
    """Returns True if file has no blank lines.
    
    Note: Does not test whether text_file is a text file."""
    with open(text_file) as tf:
        for line in tf:
            if not line.rstrip():
                return False
    return True


def linkify(string_raw):
    """docstring"""
    if "<a href=" in string_raw:
        return string_raw
    return re.compile(URL_PATTERN).sub(r'<a href="\1">\1</a>', string_raw)


def ls_visible(cwd=os.getcwd()):
    """Do I need to break this out into separate function?"""
    os.chdir(cwd)
    return [name for name in glob.glob("*")]
