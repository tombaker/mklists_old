def load_files2dirs(files2dirs):
    """
    Reads yaml dictionary mapping filenames to destination directories.
    """
    with open(files2dirs) as yamlfile:
        config = yaml.load(yamlfile)
    return config

def load_config(config_file='_mklists.yaml'):
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
    globlines_list = []
    for file in glob.glob('*'):
        globlines_list.append(file.readlines())
    return globlines_list
    [name for name in glob.glob('*') if os.path.isfile(name)]
    """
    return cwd

def load_rules(*rules_files):
    """
    Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')
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
                valid_chars = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)
        if it gets this far:
            append line to rules_l

    return rules_l (list of five-item tuples)
    """
    pass

import yaml

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

