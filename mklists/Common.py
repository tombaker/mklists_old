import os
import string
import re

__all__ = ['ls_files', 'linkify']

# Rule errors
class RuleError(SystemExit): 
    pass

# Data errors
class NotUTF8Error(SystemExit):
    """Object is not UTF8-encoded."""



class NotValidFilenameError(SystemExit): 
    pass

class NotIntegerError(SystemExit): 
    pass

class SourceNotPrecedentedError(SystemExit): 
    pass

class SourceEqualsTargetError(SystemExit): 
    pass

class RegexError(SystemExit):
    pass

# Eventually, add check whether set in '.mklistsrc' and, if so, override
VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)


