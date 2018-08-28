"""Datadir module"""

import os
import re
from mklists import (
    BadFilenameError,
    BlankLinesError,
    DatadirHasNonFilesError,
    NoDataError,
    NotUTF8Error)


def get_datalines(ls=[], but_not=[]):
    """Returns list of all lines in all files in data directory.

    Args:
        ls: list of all visible objects in data directory.
        but_not: list of patterns that match invalid filenames.

    Raises:
        DatadirHasNonFilesError: if any visible object is not a file.
        BadFilenameError: if any filename matches a bad pattern
        UnicodeDecodeError: if any file is not UTF8-encoded.
        BlankLinesError: if any file is found to have blank lines.
        NoDataError: if, in the end, there is no data to process.
    """
    _visible_files_are_really_files(ls)
    _names_of_visible_files_are_all_valid(ls, but_not)
    _visible_files_are_utf8_encoded(ls)
    return _get_datalines_from_visible_files(ls)

def _visible_files_are_really_files(objects_list):
    """Returns true if all visible objects in directory are files.

    Raises:
        DatadirHasNonFilesError: if object is not a file.
    """
    for object in objects_list:
        if not os.path.isfile(object):
            raise DatadirHasNonFilesError(f'{object} not a file.')
    return True

def _names_of_visible_files_are_all_valid(files_list, except_for):
    """Return True if no filenames match bad patterns.

    Used to block execution of mklists if the data
    folder has any files that should not be processed,
    such as temporary files or backup files.

    Raises:
        BadFilenameError: if filename matches a bad pattern.
    """
    if except_for:
        for filename in files_list:
            for bad_pat in except_for:
                if re.search(bad_pat, filename):
                    raise BadFilenameError(f'{repr(bad_pat)} in {filename}.')
    return True

def _visible_files_are_utf8_encoded(files_list):
    """Returns True if all data files are UTF8-encoded.

    Raises:
        UnicodeDecodeError: if any file is not UTF8-encoded.
    """
    for filename in files_list:
        try:
            open(filename).read()
        except UnicodeDecodeError:
            raise NotUTF8Error(f'File {filename} is not UTF8-encoded.')
    return True

def _get_datalines_from_visible_files(files_list):
    """Returns consolidated list of datalines to process.

    Raises:
        BlankLinesError: if a file is found to have blank lines.
        NoDataError: if there is no data to process at all.
    """
    aggregated_list_of_lines = []
    for file in files_list:
        for line in file.readlines():
            if not line:
                raise BlankLinesError(f'{repr(file)} has blank lines.')
            aggregated_list_of_lines.append(line)
    if not aggregated_list_of_lines:
        raise NoDataError('No data to process.')
    return aggregated_list_of_lines

