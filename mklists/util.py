from mklists.exceptions import NotUTF8Error

def is_utf8(file):
    try:
        open(file).read(512)
    except UnicodeDecodeError as e:
        raise NotUTF8Error(f'File {file} not UTF-8: convert or delete, then retry.') from e

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

def abs_pathname(pathname):
    """
    Given: 
    * the relative or absolute pathname of a file or directory

    Returns: 
    * the absolute name, if the file or directory exists
    * None, if the file or directory does not exit

    >>> abs_pathname('./mklists.py')
    '/Users/tbaker/github/tombaker/mklists/mklists/mklists.py'
    >>> abs_pathname('/Users/tbaker/github/tombaker/mklists/mklists/mklists.py')
    '/Users/tbaker/github/tombaker/mklists/mklists/mklists.py'
    >>> abs_pathname('~/github/tombaker/mklists')
    '/Users/tbaker/github/tombaker/mklists'
    >>> abs_pathname('../../../../github/tombaker/mklists')
    '/Users/tbaker/github/tombaker/mklists'
    >>> abs_pathname('../github/tombaker/mklists')
    """
    absolute_pathname = os.path.abspath(os.path.expanduser(pathname))
    if os.path.exists(absolute_pathname):
        return absolute_pathname
    else:
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
def urlify_string(s):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
    if '<a href=' in s:
        return s
    return URL_REGEX.sub(r'<a href="\1">\1</a>', s)

if __name__ == "__main__":
    is_utf8('_non-text.png')
    #is_utf8('testme.py')
    print("Apparently it did not raise an exception.")
    # filesanddestinations   = getfiles2dirs('/Users/tbaker/Dropbox/uu/agenda/.mklists.yaml')
    import doctest
    doctest.testmod()
