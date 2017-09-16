# File (contents)
#     print(repr(file))
#         NotUTF8Error('File not UTF-8: convert encoding or delete file, then retry.'
#     print(repr(file))
#         BlankLinesError('File has blank lines: delete blank lines or delete file.')
# 
# Filename (blacklisted regex)
#     print(repr(filename))
#         FilenamePatternError('Filename matches pattern {}: rename file.'.format(pattern))
#             Not start with a dot
#             Not end with ~
#             Not end with .bak
#             Not end with .tmp
#             Not have any spaces (though this comes out in course of parsing rule string)
#         FilenameCharError('Has characters not in...')
#             valid_chars = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)
#             print("Filename %r has one or more characters other than: %r" % rule, valid_chars)
# 
# Directory
#     print(repr(dirname))
#         DirNotExistError('Directory does not exist or is not accessible - skipping.'
#     print(repr(dirname))
#         NoDataError('No data here to back up or process - skipping.')

# def ls_files(filenames=os.listdir(), config_file='mklists.yaml'):
#     """
#     Arguments:
#     * filenames - default: os.listdir()
#     * config_file - default: 'mklists.yaml'
# 
#     Checks 
#     * first, for filenames matching showstopping patterns (swap filenames, backup filenames...)
#     * then, filters out filenames 
# 
#     Returns: 
#     * list of passing filenames, only for files
# 
#     FACTOR OUT ls_files_only??  
#     * [f for f in passing_filenames if os.path.isfile(f)]
#     * mustbetext?
#     """
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

