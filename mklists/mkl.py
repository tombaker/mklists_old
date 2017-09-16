import glob
import os
import re
import sys
import yaml
import pprint

class ListLine(object):
    """@@@"""

    def __init__(self, line_of_list):
        self.line = line_of_list

    def linkified_line(self):
        """
        """
        URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
        if '<a href=' in self.line:
            return self.line
        return URL_REGEX.sub(r'<a href="\1">\1</a>', self.line)

def urlify_string(s):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
    if '<a href=' in s:
        return s
    return URL_REGEX.sub(r'<a href="\1">\1</a>', s)

def get_globlines(cwd=os.getcwd()):
    """Something like:
    globlines_list = []
    for file in glob.glob('*'):
        globlines_list.append(file.readlines())
    return globlines_list
    [name for name in glob.glob('*') if os.path.isfile(name)]
    """
    return cwd

class RuleLine(object):
    def __init__(self, text_line):
        line = text_line

    def strip_comments(line):
        return line.partition('#')[0]

def get_config(config_file='_mklists.yaml'):
    with open(config_file) as yamlfile:
        config = yaml.load(yamlfile)

    files2dirs         = config['files2dirs']
    filename_blacklist = config['filename_blacklist']
    rules_files        = config['rules_files']

    pprint.pprint(config['files2dirs'])
    pprint.pprint(config['filename_blacklist'])

    print(config['files2dirs']['agendaz'])

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


def getfiles2dirs(files2dirs):
    """
    Reads yaml dictionary mapping filenames to destination directories.
    """
    with open(files2dirs) as yamlfile:
        config = yaml.load(yamlfile)
    return config

if __name__ == "__main__":
    is_utf8('_non-text.png')
    #is_utf8('testme.py')
    print("Apparently it did not raise an exception.")
    # filesanddestinations   = getfiles2dirs('/Users/tbaker/Dropbox/uu/agenda/.mklists.yaml')
