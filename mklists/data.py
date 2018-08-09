from dataclasses import dataclass

@dataclass
class Datadir:
    pathname: str = "."

    def get_data(self):
        """\
        _datadir_exists()
        for filename in filenames
            _no_invalid_filenames()
            _files_visible()
            return aggregated lines
        """
        datalines = []
        for file in self.filenames
            datalines.append(file.readlines())
        return datalines

    def _datadir_exists(self):
        """NoDatadirError('Directory does not exist or is not accessible.')"""

    def _no_invalid_filenames(self):
        """FilenamePatternError - config['invalid_filenames']"""

    def _files_visible(self):
        # change directory?
        ls_visible_files = [name for name in glob.glob('*')]
        self.filenames = ls_visible_files

@dataclass
class Datafile:

    def get_datalines(self):
        """\
        _is_file()
        _has_data()
        _has_no_blank_lines()
        _is_text()
        _is_utf8_encoded()
        returns self.datalines, a list"""

    def _has_data(self):
        """NoDataError('No data here to back up or process - skipping.')"""

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

    def linkify(self):
        datalines_linkified = []
        for line in self.datalines:
            if '<a href=' in line:
                return line
            line = re.compile(URL_REGEX).sub(r'<a href="\1">\1</a>', string)

    
