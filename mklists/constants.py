"""@@@Docstring"""

import datetime

# Time stamp
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")

# Regular expressions
INVALID_FILENAME_REGEXES = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.,@:A-Za-z0-9]+$"

# Directory names
BACKUPDIR_NAME = ".backups"
HTMLDIR_NAME = ".html"
DATADIRA_NAME = "a"

# Configuration file
CONFIG_YAMLFILE_NAME = "mklists.yml"

CONFIG_YAMLFILE_STR = r"""# Main configuration file (required)
verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}
"""

# Rules files
RULE_YAMLFILE_NAME = ".rules"

ROOTDIR_RULES_YAMLFILE_STR = r"""# Here: Global rules, applied before folder-specific rules.
# Put here any rules that apply to multiple list folders.
# Each rule matches against part of a line of text.
# Each rule is a list with five components:
# 1. Which part of the text line will be tested for a match:
#    '0' = entire line
#    '1' = first column (whitespace-delimited field)
# 2. Regular expression to be matched against (part of) the line (as per 1, above).
# 3. Label and intended filename of source file of the text line (as per 1, above).
# 4. Label and intended filename of target file to which the line should be moved
#    if it matches the regular expression.
# 5. Sort order of the target file.
- [0, '.',       lines.tmp, alines,  0]
- [0, '201.-..', alines,    blines,  1]
"""

MINIMAL_DATADIRA_RULES_YAMLFILE_STR = r"""# Rules for Folder A.
- [0, '.',          alines,    etc.txt,  0]
- [1, 'TODO',       etc.txt,   todo.txt, 1]
"""

EXAMPLE_DATADIRA_RULES_YAMLFILE_STR = r"""
- [0, '.',       alines,     todo.txt,   1]
- [1, 'NOW',     todo.txt,   now.txt,    1]
- [1, 'LATER',   todo.txt,   later.txt,  0]
"""

EXAMPLE_DATADIRB_RULES_YAMLFILE_STR = r"""# Rules for folder B - appended to global rules.
- [0, '.',       lines,      blines,     0]
- [1, '^2019',   blines,     2019.txt,   1]
- [1, '^2020',   blines,     2020.txt,   0]
"""

EXAMPLE_DATADIRA_TEXTFILE_STR = r"""\
TODO Examine the configuration file 'mklists.yml' (in the root directory); tweak if needed.
TODO Examine the '.rules' file (in the root directory); tweak if needed.
TODO Examine 'a/.rules' file in subdirectory 'a' (under root directory; tweak if needed.
TODO 2019-08-14 Installed mklists <= edit: remove "TODO", replace date - will end up in 'b/log.txt'.
LATER According to default rules, this line will end up in 'etc.txt'.
"""
