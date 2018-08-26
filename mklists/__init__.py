"""Marks as package directory for Python."""

import string

VALID_FILENAME_CHARS = """\
:@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""

MKLISTSRC = '.mklistsrc'

RULEFILE = '.rules'

DEFAULT_RULE_FILE = """\
- [0,  '.',         lines,         todo.txt,   0]  # notes...
- [1,  'NOW',       todo.txt,      now.txt,    0]  # notes...
- [1,  'LATER',     todo.txt,      later.txt,  0]  # notes...
"""
