"""Marks mklists package directory, sets constants."""

MKLISTSRC = '.mklistsrc'

VALID_FILENAME_CHARS = """\
:@-_=.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""

GLOBAL_RULEFILE_NAME = '.globalrules'

GLOBAL_RULEFILE_STARTER = """\
- [0,  '.',         lines,         todo.txt,   0]  # notes...
"""

LOCAL_RULEFILE_NAME = '.rules'

LOCAL_RULEFILE_STARTER = """\
- [1,  'NOW',       todo.txt,      now.txt,    0]  # notes...
- [1,  'LATER',     todo.txt,      later.txt,  0]  # notes...
"""
