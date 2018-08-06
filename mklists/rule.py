import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

class NotFiveFieldsError(SystemExit): pass

@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0


    def has_five_fields(self):
        if len([v for v in self.__dict__.values() if v is not None]) != 5:
            raise NotFiveFieldsError
            #sys.exit()

