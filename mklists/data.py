import glob
import os
import re
from dataclasses import dataclass
from mklists import *


@dataclass
class Datadir:
    dirname: str = '.'
    bad_filename_patterns: tuple = tuple()

    def get_datalines(self):
        try:
            os.chdir(self.dirname)
            self.visible_pathnames = [name for name in glob.glob('*')] 
        except FileNotFoundError:
            raise NoDatadirError('Directory is not accessible.')
        self._visible_pathnames_are_all_files()
        self._visible_filenames_are_all_valid()
        self._visible_files_are_utf8_encoded()
        self._get_datalines_from_datafiles()

    def _visible_pathnames_are_all_files(self):
        for pathname in self.visible_pathnames:
            if not os.path.isfile(pathname):
                raise DatadirHasNonFilesError(f'{pathname} not a file.')
        return self.visible_pathnames

    def _visible_filenames_are_all_valid(self):
        for filename in self.visible_pathnames:
            for bad_pat in self.bad_filename_patterns:
                if re.search(bad_pat, filename):
                    raise BadFilenameError(f'{bad_pat} in {filename}.')
        return True

    def _visible_files_are_utf8_encoded(self):
        for filename in self.visible_pathnames:
            try:
                open(self.filename).read()
            except UnicodeDecodeError:
                raise NotUTF8Error(f'File {file} not UTF8-encoded.')
        return True

    def _get_datalines_from_datafiles(self):
        self.datalines = []
        for file in self.visible_pathnames:
            for line in file.readlines():
                if not line:
                    raise BlankLinesError(f'File {file} has blank lines.')
                self.datalines.append(line)
        if not self.datalines:
            raise NoDataError('No data here.')
        return self.datalines


class DataError(SystemExit):
    pass


class BadFilenameError(DataError):
    pass


class BlankLinesError(DataError):
    pass


class DatadirHasNonFilesError(DataError):
    pass


class NoDataError(DataError):
    pass


class NoDatadirError(DataError):
    pass


class NotUTF8Error(DataError):
    pass

