import glob
import os
import pprint
import re
import string
import sys
import yaml

from dataclasses import dataclass

__all__ = [
    'RuleError', 
    'NotUTF8Error', 
    'NotValidFilenameError', 
    'NotIntegerError', 
    'SourceNotPrecedentedError', 
    'SourceEqualsTargetError', 
    'SourcePatternError',
    'VALID_FILENAME_CHARS',
    'URL_PATTERN'
]

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

class SourcePatternError(SystemExit):
    pass

# Eventually, add check whether set in '.mklistsrc' and, if so, override
VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

URL_PATTERN = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
