"""Datadir module"""

import glob
import os
import re
from dataclasses import dataclass
from mklists import (
    BadFilenameError,
    BlankLinesError,
    DatadirHasNonFilesError,
    NoDataError,
    NoDatadirError,
    NotUTF8Error)


@dataclass
class Datadir:
    """docstring"""

    # dirname: str = '.'   # need? os.chdir(self.dirname) should be elsewhere?
    bad_filename_patterns: list = None
    visible_files: list = None
    datalines: list = None

    def get_datalines(self):
        """Gets data lines from all files in a given directory.

        Calls private methods to check that all visible objects
        in a given directory are UTF8-encoded files, with no
        temporary or backup files (i.e., files matching a list
        of bad filename patterns).

        Returns:
            self.visible_files: list of data files in given directory.
            self.datalines: list of all lines in all valid data files.

        Raises:
            NoDatadirError: if directory is not accessible.
            DatadirHasNonFilesError: if any visible object is not a file.
            BadFilenameError: if any filename matches a bad pattern
            UnicodeDecodeError: if any file is not UTF8-encoded.
            BlankLinesError: if any file has blank lines.
            NoDataError: if there is no data to process.
        """
        try:
            self.visible_files = [name for name in glob.glob('*')]
        except FileNotFoundError:
            raise NoDatadirError('Directory is not accessible.')
        self._visible_files_are_really_files()
        self._names_of_visible_files_are_all_valid()
        self._visible_files_are_utf8_encoded()
        self._get_datalines_from_visible_files()

    def _visible_files_are_really_files(self):
        """Confirms that all visible objects in directory are files.

        Returns:
            True

        Raises:
            DatadirHasNonFilesError: if object is not a file.
        """
        for pathname in self.visible_files:
            if not os.path.isfile(pathname):
                raise DatadirHasNonFilesError(f'{pathname} not a file.')
        return True

    def _names_of_visible_files_are_all_valid(self):
        """Confirms that no filenames match bad patterns.

        Used to block execution of mklists if the data
        folder has any files that should not be processed,
        such as temporary or backup files.

        Returns:
            True

        Raises:
            BadFilenameError: if filename matches a bad pattern.
        """
        for filename in self.visible_files:
            # add: if self.bad_filename_patterns is not None:
            for bad_pat in self.bad_filename_patterns:
                if re.search(bad_pat, filename):
                    raise BadFilenameError(f'{bad_pat} in {filename}.')
        return True

    def _visible_files_are_utf8_encoded(self):
        """Checks that all data files are UTF8-encoded.

        Returns:
            True

        Raises:
            UnicodeDecodeError: if any file is not UTF8-encoded.
        """
        for filename in self.visible_files:
            try:
                open(filename).read()
            except UnicodeDecodeError:
                raise NotUTF8Error(f'File {filename} not UTF8-encoded.')
        return True

    def _get_datalines_from_visible_files(self):
        """Returns consolidated list of datalines to process.

        Raises:
            BlankLinesError: if any file has blank lines.
            NoDataError: if there is no data to process.
        """
        self.datalines = []
        for file in self.visible_files:
            for line in file.readlines():
                if not line:
                    raise BlankLinesError(f'{repr(file)} has blank lines.')
                self.datalines.append(line)
        if not self.datalines:
            raise NoDataError('No data to process.')
        return self.datalines

