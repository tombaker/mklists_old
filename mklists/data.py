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

    def _visible_filenames_are_all_valid(self):
        for filename in self.visible_pathnames:
            for bad_pat in bad_filename_patterns:
                if re.search(bad_pat, filename):
                    raise BadFilenameError(f'{bad_pat} in {filename}.')

    def _visible_files_are_valid_datafiles(self):
        for filename in self.visible_pathnames:
            Datafile.validate(filename)

    def _get_datalines_from_datafiles(self):
        datalines = []
        for file in self.visible_pathnames:
            datalines.append(file.readlines())
        if not datalines:
            raise NoDataError('No data here')
        return datalines

@dataclass
class Datafile:

    def validate(self):
        _is_file()
        _has_data()

    def _is_file(self):
        """\
        Visible pathnames in Datadir must all be files:
        * os.path.isfile(name)
        * no directories, no links
        """

    def _is_text(self):
        """flag - has arbitrary allowable percent non-ASCII characters"""

    def _is_utf8_encoded(self):
        try:
            open(self.filename).read()
        except UnicodeDecodeError:
            raise NotUTF8Error(f'File {file} not UTF8-encoded.')

    def _has_no_blank_lines(self):
        """BlankLinesError('File has blank lines.')"""

    def get_datalines(self):
        """\
        _has_no_blank_lines()
        _is_text()
        _is_utf8_encoded()
        returns self.datalines, a list"""

    def linkify(self):
        datalines_linkified = []
        for line in self.datalines:
            if '<a href=' in line:
                return line
            line = re.compile(URL_REGEX).sub(r'<a href="\1">\1</a>', string)

    
