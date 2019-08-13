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

MINIMAL_DATADIRA_RULES_YAMLFILE_STR = r"""\
- [0, '.',       lines,      consolidated_lines,   0]"""

ROOTDIR_RULES_YAMLFILE_STR = r"""# Global rules, applied before rules specific to a list folder.
# Put here any rules that apply to multiple list folders.
- [0, '.',          x,         lines,            0]
- [1, 'NOW',        lines,     alines,           1]
- [1, 'LATER',      lines,     alines,           1]
- [0, '^2019|2020', lines,     blines,           1]"""

EXAMPLE_DATADIRA_RULES_YAMLFILE_STR = r"""# Rules for folder A - appended to global rules.
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       alines,     todo.txt,   1]
- [1, 'NOW',     todo.txt,   now.txt,    1]
- [1, 'LATER',   todo.txt,   later.txt,  0]
"""

EXAMPLE_DATADIRB_RULES_YAMLFILE_STR = r"""# Rules for folder B - appended to global rules.
- [0, '.',       lines,      blines,     0]
- [1, '^2019',   blines,     2019.txt,   1]
- [1, '^2020',   blines,     2020.txt,   0]
"""
