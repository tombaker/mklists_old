from dataclasses import dataclass

@dataclass
class Datadir:
    dirname: str = '.'
    bad_filename_patterns: list

    def get_datalines(self):
        _change_to_datadir()
        _visible_pathnames_are_all_files()
        _visible_filenames_are_all_valid()
        _visible_files_are_valid_datafiles()
        _get_datalines_from_datafiles()

    def _change_to_datadir(self):
        try:
            os.chdir(self.dirname)
        except FileNotFoundError:
            raise NoDatadirError('Directory is not accessible.')

    def _visible_pathnames_are_all_files(self):
        self.visible_pathnames = [name for name in glob.glob('*')] 
        for pathname in self.visible_pathnames:
            if not os.path.isfile(pathname):
                raise DatadirHasNonFilesError(f'{pathname} not a file.')
        return self.visible_pathnames

    def _visible_filenames_are_all_valid(self):
        for filename in self.visible_pathnames:
            for bad_pat in bad_filename_patterns:
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

