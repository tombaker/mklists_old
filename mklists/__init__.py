"""Defines Mklists constants and exception classes."""

import datetime

TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
INVALID_FILENAME_PATTERNS = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
CONFIGFILE_NAME = "mklists.yml"  # only in root directory
CONFIG_STARTER_DICT = {}
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.@:A-Za-z0-9]+$"
RULEFILE_NAME = ".rules"
BACKUP_DIR_NAME = "_backups"
HTMLFILES_DIR_NAME = "_html"

CONFIGFILE_YAMLSTR = r"""\
backups: 3
html: false
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
verbose: false
global_rules:
- [0, '.',          all_lines, lines,    0]
- [0, '^=',         all_lines, move_to_a.txt, 1]
- [0, '^2019|2020', all_lines, move_to_logs.txt, 1]
files2dirs:
- move_to_logs.txt: logs
- move_to_a.txt: a
"""

RULEFILE_STARTER_YAMLSTR = """\
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       to_a.txt    todo.txt,   1]
- [1, 'NOW',     todo.txt,    now.txt,   1]
- [1, 'LATER',   todo.txt,  later.txt,   0]
"""
