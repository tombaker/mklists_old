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
DATADIRB_NAME = "b"

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

ROOTDIR_RULES_YAMLFILE_STR = r"""# Global rules, applied before folder-specific rules.
#
# Each rule matches against part of a line of text.
#
# Each rule is a list with five components:
# 1. Section of text line (integer) to be matched against regular expression:
#    0 = entire line
#    2 = second column (whitespace-delimited field)
# 2. Regular expression against which the line will be matched.
# 3. Filename of text line to be matched (see 1, above).
# 4. Filename of target file where text line should be moved if it matches.
# 5. Sort order (integer) of target file.
#    0 = will sort on entire line
#    2 = will sort on second column (whitespace-delimited field)
#
# Note:
#   Integer values (1 and 5) must _not_ be quoted ("2"); this turns them into strings.
#   If regular expressions contain backslashes, these must be escaped (e.g., "\\").
#   Filenames (3 and 4) must be composed of valid characters.
#   * In the YAML file, quotes may be omitted around filenames (unless the filenames
#   * look like numbers).
#   * By default, pathname slashes ('/'), spaces, and accented characters are illegal.
#   * Set of valid filename characters can be configured in 'mklists.yml'.

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

EXAMPLE_DATADIRB_TEXTFILE_STR = r"""\
TODO Note how the default rules will move this line to Folder A.
"""
