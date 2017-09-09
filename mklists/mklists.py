from collections import defaultdict
import glob
import os
import re

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

def istext(file_to_test):
    class NotUTF8Error(Exception): pass
    try:
        open(file_to_test).read(512)
    except UnicodeDecodeError:
        raise SystemExit('File {} not text in UTF-8; try converting.'.format(file_to_test))

def get_rules(*rules_files):
    """
    split line once on hash (#)
    keep half of line before hash
    strip whitespace on both sides
    delete blank lines
    rules_l = list()
    for line in rules_l:
        line_split = line.split()
        Something like for line, line_split in ..
        
        split the line 
        bail (citing line) if any line is not exactly five fields long
        try:
            $1.isdigit()  - which includes zero
            $5.isdigit()  - which includes zero
            $1 = int($1)
            $5 = int($1)
        except SourceMatchAndTargetSortOrderDigits:
            bail (citing line) with error message
        $3 = re.compile($3)
        $4 and $5:
            must have only permitted characters
        if it gets this far:
            append line to rules_l

    return rules_l (list of five-item tuples)
    """
    pass

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
    """
    return cwd

class RuleLine(object):

    def __init__(self, text_line):
        line = text_line

    def strip_comments(line):
        return line.partition('#')[0]


