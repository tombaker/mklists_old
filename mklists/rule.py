import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass
from typing import List

class NotFiveFieldsError: pass

@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: str = None


    def has_five_fields(self):
        # as per constructor, will always be 5 keys
        # change so that it all values must be not None?
        if len(self.__annotations__.keys()) != 5:
            #raise NotFiveFieldsError
            sys.exit()

