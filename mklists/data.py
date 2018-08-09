from dataclasses import dataclass

@dataclass
class Datadir:
    where: str

    def ls_visible_files(folder='.'):
        visible_files = [name for name in glob.glob('*')
                         if os.path.isfile[name]]
        return visible_files


@dataclass
class Datafile():
    file = click.Path
    # is_utf8_encoded()
    # file has legal name (only allowable characters - e.g., no spaces)
    # is_text (implement this?)
    #   allowable_percent_non_ascii_characters
    #   return True or False
    # return { file: [['one line\n'], [...]] }
    #     return [f for f in passing_filenames if os.path.isfile(f)]

def linkify(string):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)""")
    if '<a href=' in string:
        return string
    return URL_REGEX.sub(r'<a href="\1">\1</a>', string)


def _is_utf8_encoded(filename):
    try:
        open(filename).read()
    except UnicodeDecodeError as e:
        raise NotUTF8Error(f'File "{file}" is not UTF-8-encoded. Convert to UTF-8 or delete before proceeding.') from e

def ls_files(filenames=os.listdir(), config_file='mklists.yaml'):
    """
    Arguments:
    * filenames - default: os.listdir()
    * config_file - default: 'mklists.yaml'

    Checks 
    * first, for filenames matching showstopping patterns (swap filenames, backup filenames...)
    * then, filters out filenames 

    Returns: 
    * list of passing filenames, only for files

    FACTOR OUT ls_files_only??  
    * [f for f in passing_filenames if os.path.isfile(f)]
    * mustbetext?
    """

    #     with open(config_file) as mkl:
    #         config = yaml.load(mkl)
    #         
    #     no_showstoppers = []
    #     for filename in filenames:
    #         for regex_string in config['showstopping_filenames']:
    #             if re.search(regex_string, os.path.split(filename)[1]):
    #                 raise SystemExit("Show-stopper: filename {} matches blacklist pattern {}".format(filename, regex_string))
    #         no_showstoppers.append(filename)
    # 
    #     passing_filenames = []
    #     for filename in no_showstoppers:
    #         for regex_string in config['ignored_filenames']:
    #             if not re.search(config['ignored_filenames'][0], filename):
    #                 passing_filenames.append(filename)
    # 
    #     return [f for f in passing_filenames if os.path.isfile(f)]

def linkify(string):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)""")
    if '<a href=' in string:
        return string
    return URL_REGEX.sub(r'<a href="\1">\1</a>', string)

def load_globlines(cwd=os.getcwd()):
    """Something like:
    globlines_l = []
    for file in glob.glob('*'):
        globlines_l.append(file.readlines())
    return globlines_l
    [name for name in glob.glob('*') if os.path.isfile(name)]
    """
    return cwd

def load_data(files):
    """
    File (contents)
        print(repr(file))
            NotUTF8Error('File not UTF-8: convert encoding or delete file, then retry.'
        print(repr(file))
            BlankLinesError('File has blank lines: delete blank lines or delete file.')
    
    Filename (blacklisted regex)
        print(repr(filename))
            FilenamePatternError('Filename matches pattern {}: rename file.'.format(pattern))
                Not start with a dot
                Not end with ~
                Not end with .bak
                Not end with .tmp
                Not have any spaces (though this comes out in course of parsing rule string)
    
    Directory
        print(repr(dirname))
            DirNotExistError('Directory does not exist or is not accessible - skipping.'
        print(repr(dirname))
            NoDataError('No data here to back up or process - skipping.')
    """
