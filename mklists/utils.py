"""Utility module"""

import os
import re
import glob
from mklists import URL_PATTERN


def is_file(object_path):
    """Returns True if object is a file.

    Raises:
        DatadirHasNonFilesError: if object is not a file.
    """
    if not os.path.isfile(object_path):
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
    """docstring"""
    if '<a href=' in string_raw:
        return string_raw
    return re.compile(URL_PATTERN).sub(r'<a href="\1">\1</a>', string_raw)

def ls_visible(cwd=os.getcwd()):
    """Do I need to break this out into separate function?"""
    os.chdir(cwd)
    return [name for name in glob.glob('*')]
