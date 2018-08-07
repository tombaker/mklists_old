import os
import re

__all__ = ['_is_utf8_encoded', 'ls_files', 'abs_pathname', 'linkify']

"""According to Martelli, the simplest way to share objects 
(such as functions and constants) among modules in package P:
    
Group shared objects in file P/Common.py.

Then:
    -- `import Common` 
       from every module in package that needs to access the objects
       -- refer to Common.f, Common.K...
"""

class NotUTF8Error(SystemExit):
    """Exit with helpful error message if object is not UTF-8."""


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

def linkify(string):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)""")
    if '<a href=' in string:
        return string
    return URL_REGEX.sub(r'<a href="\1">\1</a>', string)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

def load_config(config_file='_mklists.yaml'):
    """ Loads files with yaml configuration dictionary.
    """
    with open(config_file) as yamlfile:
        config = yaml.load(yamlfile)

    files2dirs         = config['files2dirs']
    filename_blacklist = config['filename_blacklist']
    rules_files        = config['rules_files']

    pprint.pprint(config['files2dirs'])
    pprint.pprint(config['filename_blacklist'])

    print(config['files2dirs']['agendaz'])

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
            FilenameCharError('Has characters not in...')
                valid_chars = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)
                print("Filename %r has one or more characters other than: %r" % rule, valid_chars)
    
    Directory
        print(repr(dirname))
            DirNotExistError('Directory does not exist or is not accessible - skipping.'
        print(repr(dirname))
            NoDataError('No data here to back up or process - skipping.')
    """

# Put this into default .mklistsrc
CORRECT_RULE_FORM = """\
The rule above is incorrectly formed.

Rule must have four or (optionally) five fields:

    3 /x/ a.txt b.txt
    3 /x/ a.txt b.txt 2   # with optional sort order

Fields:

    1. Field against which regex is matched (a digit).
    2. Regex, delimited by slashes.
    3. Source file, lines of which are tested for matches.
    4. Target file, destination of matching lines.
    5. Sort order of target file

In pseudo-code:

    for each line in source a.txt
        if regex /x/ matches third field (the "match field")
            move line from a.txt to b.txt
            sort b.txt on second field (if optional sort order given)
        if regex /x/ does not match third field
            do nothing

Note:
-- If match field is 0, entire line (with whitespace) matched.
-- If match field is greater than line length, match is ignored.
-- Regex must escape forward slashes - eg "/\/n/".
-- Regex may include spaces - eg "/^From /"
-- Whitespace is ignored except within regex (between first and last slash).
-- Comments (everything after a pound sign) are ignored.
-- Fields 3 and 4 are (configurably) valid filenames not containing slashes.
"""
