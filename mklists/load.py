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

