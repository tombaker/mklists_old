"""Datafile module

Refactor as get_datalines(file) instead of get_datalines(ls)?
"""

import os
import re
import string
from mklists import (
    URL_PATTERN,
    BadFilenameError,
    BlankLinesError,
    DatadirHasNonFilesError,
    NoDataError,
    NotUTF8Error)

def get_lines(object):
    all_lines = []
    if not is_file(object):
        print("All visible objects in current directory must be files.")
        raise DatadirHasNonFilesError(f'{object} is not a file.')
    if not has_valid_name(object, bad_names=ctx.obj['invalid_filename_patterns']):
        print("Invalid filename patterns are intended to detect the "
              "presence of backup files, temporary files, and the like.")
        raise BadFilenameError(f"{repr(object)} matches one of "
                               "{ctx.obj['invalid_filename_patterns']}.")
    if not is_utf8_encoded(object):
        print("All visible files in data directory must be UTF8-encoded.")
        raise NotUTF8Error(f'File {object} is not UTF8-encoded.')
    with open(object) as rfile:
        for line in rfile:
            if not line:
                print("No file in data directory may contain blank lines.")
                raise BlankLinesError(f'{repr(object)} has blank lines.')
            all_lines.append(line)

    return all_lines

def is_file(path_object):
    """Returns True if object is a file.

    Raises:
        DatadirHasNonFilesError: if object is not a file.
    """
    if not os.path.isfile(path_object):
        return False
    return True

def has_valid_name(filename, bad_names):
    """Return True if no filenames match bad patterns.

    Used to block execution of mklists if the data
    folder has any files that should not be processed,
    such as temporary files or backup files.

    Raises:
        BadFilenameError: if filename matches a bad pattern.
    """
    for bad_pattern in bad_names:
        if re.search(bad_pattern, filename):
            print(f"{repr(bad_pattern)} in {filename}.")
            return False
    return True

# Note: is_utf8_encoded, has_no_blank_lines
def is_utf8_encoded(file):
    """Returns True if all data files are UTF8-encoded.

    Raises:
        UnicodeDecodeError: if any file is not UTF8-encoded.
    """
    try:
        open(file).read()
    except UnicodeDecodeError:
        return False
    return True

def has_no_blank_lines(text_file):
    """Note: Does not test whether test file"""
    for line in text_file:
        if not line:
            return False
    return True

def linkify(string_raw):
    if '<a href=' in string_raw:
        return string_raw
    return re.compile(URL_PATTERN).sub(r'<a href="\1">\1</a>', string_raw)
    
