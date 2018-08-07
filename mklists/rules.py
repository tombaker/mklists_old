import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass

class BadRuleString(SystemExit): 
    pass

@dataclass
class RulestringParser:

    def get_stringlines(self, *rulefiles):
        stringlines = []
        for rf in rulefiles:
            try:
                with open(rf, 'r') as rulefile:
                    stringlines.extend(rulefile.read().splitlines())
            except FileNotFoundError:
                sys.exit(f'Rule file "{rf}" does not exist or is not accessible.')
        self.stringlines = stringlines
        return self.stringlines

    def parse_stringlines_to_splitlines(self):
        splitlines = []
        for line in self.stringlines:
            line_fielded = []
            line_field1, __, line_rest = line.partition('/')
            line_fielded.append(line_field1.strip())
            regex, __, line_rest = line_rest.rpartition('/')
            line_fielded.append(regex)
            line_rest = line_rest.partition('#')[0].strip()
            line_fielded.extend(line_rest.split())
            line_fielded = [field for field in line_fielded if not re.match('#', field)]
            line_fielded = [field for field in line_fielded if field]
            if line_fielded:
                splitlines.append(line_fielded)
        self.splitlines = splitlines
        return self.splitlines
                        
