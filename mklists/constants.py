"""For initializing pseudo-constants: global variables not intended to be changed."""

import datetime


BACKUPS_DIR_NAME = "_backups"
HTMLDIR_NAME = "_html"
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.,@:A-Za-z0-9]+$"
DATADIRA_README_FILE_NAME = "README.txt"
DATADIRA_README_FILE_CONTENTS = (
    "NOW Examine 'a/.rules' file (in this directory); edit as needed.\n"
    "NOW Hint: Examine '.rules' file in root directory; leave unchanged for now..\n"
    "NOW Hint: Change beginning of this line to today's date (eg, 2020-01-17).\n"
    "NOW Hint: Then run 'mklists' to see what happens to these lines.\n"
    "NOW Change the name of this directory, as needed.\n"
    "NOW If you already understand 'mklists', replace these lines with your own.\n"
    "LATER Check out 'mklists.yml' in the root directory.\n"
    "LATER Hint: Create 'b' directory as a destination for 'log.txt'.\n"
)
RULEFILE_NAME = ".rules"
ROOTDIR_RULEFILE_NAME = "rules.cfg"
ROOTDIR_RULEFILE_CONTENTS = (
    "# Global rules.\n"
    "in field|match |in source  |move to    |sort by|\n"
    "0       |.     |lines.tmp  |lines      |1      |Comments here.\n"
)
DATADIRA_NAME = "a"
DATADIRA_RULEFILE_CONTENTS = (
    "# First five fields in lines that start with integers are parsed as rules.\n"
    "# Everything else - empty lines, comments, extra fields - is ignored.\n"
    "# For readability, fields may contain whitespace on the left or right.\n"
    "# 1. Field in source line to be matched.\n"
    "#    Value '0' means 'match anywhere in line'.\n"
    "# 2. Regex matched against the source field or line.\n"
    "#    Regex may contain spaces: '|   ^2020 ..  |' = regex '^2020 ..'.\n"
    "# 3. Source: in-memory set of lines _from_ which lines matching regex are moved.\n"
    "# 4. Target: in-memory set of lines _to_ which lines matching regex are moved.\n"
    "# 5. Field by which target is to be sorted.\n"
    "#    Value '0' means 'sort on entire line'.\n"
    "#    Absence of a value (blank field) means 'do not sort'.\n"
    "# At the end, non-empty sources and targets are written to files.\n"
    "\n"
    "in field|match |in source  |move to    |sort by|\n"
    "0       |.     |lines      |todo.txt   |1      |Comments here.\n"
    "1       |NOW   |todo.txt   |now.txt  |1      |Pipe delimiters need not align.\n"
    "1       |LATER |todo.txt   |later.txt  |       |'later.txt' will not be sorted.\n"
    "1       |^2020 |todo.txt   |log.txt    |0      |\n"
)
CONFIG_YAMLFILE_NAME = "mklists.yml"

# pylint: disable=anomalous-backslash-in-string
# => the slashes in "invalid filename patterns" are valid in YAML
CONFIG_YAMLFILE_CONTENT = (
    "verbose: True\n"
    "htmlify: True\n"
    "backup_depth: 3\n"
    "invalid_filename_patterns:\n"
    "- \.swp$\n"
    "- \.tmp$\n"
    "- ~$\n"
    "- ^\.\n"
    "\n"
    "# # For given file, destination directory to which it should be moved\n"
    "# files2dirs:\n"
    "#     to_a.txt: a\n"
    "#     to_b.txt: b\n"
    "#     to_c.txt: /Users/foo/logs\n"
)
