from collections import defaultdict
import glob
import os
import re
import sys

def shuffle(rules_l, globlines_l):
    """Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')"""

    # Initialize dictionary mkl_d (where everything happens) with:
    # -- key: rule.source
    # -- value: globlines_l, an aggregated list of lines from all text files in working directory
    mkl_d = defaultdict(list)
    mkl_d[rules_l[0].src] = globlines_l

    for rule in rules_l:
        for ln in mkl_d[rule.src]:
            awkf    = rule.srcmatch_awkf
            ethf    = rule.srcmatch_awkf - 1
            rgx     = rule.srcmatch_rgx
            trg     = rule.trg
            src     = rule.src

            # if awkf out of range, then src and trg remain unchanged
            # in srcmatch_awkf, zero means "match against entire line"
            if awkf > len(ln.split()):
                continue                       

            # if awkf is zero, then regex matched against entire line
            if awkf == 0:                
                mkl_d[trg].extend([ln for ln in mkl_d[src] if re.search(rgx, ln)])
                mkl_d[src] = [ln for ln in mkl_d[src] if not re.search(rgx, ln)]

            # if awkf greater than zero (and within range), regex matched against specific field
            if awkf > 0:
                mkl_d[trg].extend([ln for ln in mkl_d[src] if re.search(rgx, ln.split()[ethf])])
                mkl_d[src] = [ln for ln in mkl_d[src] if not re.search(rgx, ln.split()[ethf])]

            # sort mkl_d[trg], dsu-style, if trgsort_awkf greater than zero (note: zero is false)
            # in trgsort_awkf, zero means "no sort order specified"
            if rule.trgsort_awkf:
                eth_sortkey = rule.trgsort_awkf - 1
                decorated = [(ln.split()[eth_sortkey], i, ln) for i, ln in enumerate(mkl_d[trg])]
                decorated.sort()
                mkl_d[trg] = [ln for grade, i, ln in decorated]
        
    return mkl_d

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

def urlify_string(s):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
    if '<a href=' in s:
        return s
    return URL_REGEX.sub(r'<a href="\1">\1</a>', s)

def is_utf8(file):
    class NotUTF8Error(SystemExit): pass
    try:
        open(file).read(512)
    except UnicodeDecodeError as e:
        raise NotUTF8Error('File {} not UTF-8: convert or delete, then retry.'.format(file)) from e

class ListLine():
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
