"""@@@Docstring"""

import datetime

# Time stamp
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")


# Regular expressions
INVALID_FILENAME_REGEXES = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.,@:A-Za-z0-9]+$"


# Names of directories
BACKUPDIR_NAME = ".backups"
HTMLDIR_NAME = ".html"


# Names of files
CONFIG_YAMLFILE_NAME = "mklists.yml"
RULE_YAMLFILE_NAME = ".rules"


# Minimal configuration
MINIMAL_CONFIG_YAMLFILE_STR = r"""verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}"""

MINIMAL_ADIR_RULES_YAMLFILE_STR = r"""\
- [0, '.',       lines,      consolidated_lines,   0]"""


# Newbie configuration files
NEWBIE_CONFIG_YAMLFILE_STR = r"""# Configuration file with comments
verbose: false
html_yes: false
backup_depth_int: 3
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
files2dirs_dict: {}"""

NEWBIE_ROOTDIR_RULES_YAMLSTR = r"""\
# This file: Global rules, applied before rules specific to a list folder.
# Put here any rules that apply to multiple list folders.
- [0, '.',          x,         lines,            0]
- [0, '^=',         lines,     move_to_a.txt,    1]
- [0, '^2019|2020', lines,     move_to_logs.txt, 1]"""

NEWBIE_DATADIRA_RULES_YAMLSTR = """\
# This file: Rules specific to this list folder.
# At runtime, these rules are appended to the global rules.
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       to_a.txt    todo.txt,   1]
- [1, 'NOW',     todo.txt,   now.txt,    1]
- [1, 'LATER',   todo.txt,   later.txt,  0]
"""

NEWBIE_DATADIRB_RULES_YAMLSTR = """\
# This file: Rules specific to this list folder.
# At runtime, these rules are appended to the global rules.
- [0, '.',       lines,      b.txt,      0]
- [1, '^2019',   b.txt,      2019.txt,   1]
- [1, '^2020',   b.txt,      2020.txt,   0]
"""
