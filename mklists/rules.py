import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass

class BadRuleString(SystemExit): 
    pass

class NotValidFilenameError(SystemExit): 
    pass

class NotIntegerError(SystemExit): 
    pass

class SourceNotPrecedentedError(SystemExit): 
    pass

class SourceEqualsTargetError(SystemExit): 
    pass

class BadRegexError(SystemExit):
    pass

# Eventually, add check whether set in '.mklistsrc' and, if so, override
VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)


@dataclass
class RulestringParser:
    """\
    Usage:
        x = RulestringParser
        x.get_stringlines('_rules', '_rules_correct')
        x.parse_stringlines_to_splitlines()
        x.splitlines_to_ruleobjects()
        x.validate_rules()
    """

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

    def splitlines_to_ruleobjects(self):
        rules = []
        for rule in self.splitlines:
            """2018-08-08: AttributeError: 'list' object has no attribute '_source_is_precedented'"""
            #Rule.validate(rule)
            rules.append(Rule(*rule))                       
        self.rules = rules
        return self.rules

    def validate_rules(self):
        validated_rules = []
        for rule in self.rules:
            Rule.validate(rule)
            validated_rules.append(rule)
        self.rules = validated_rules
        return self.rules

    def apply_rules_to(self, datalines):

        all_datalines = defaultdict(list)
        initialized = False

        for rule in rules_l:

            [match_awkf, regexp, source, target, sort_awkf] = rule
            # insert ckrules() here, possibly redundantly
            match_awkf = int(match_awkf)
            sort_awkf = int(sort_awkf)

            if not initialized:
                all_d[source] = lines_l
                initialized = True

            apply_rule(match_awkf, regexp, source, target, sort_awkf, all_d)

        return all_d


@dataclass
class Rule:
    source_matchfield: int = None
    source_matchpattern: str = None
    source: str = None
    target: str = None
    target_sortorder: int = 0

    initialized = False
    sources = []

    def _source_is_precedented(self):
        if not Rule.initialized:
            Rule.sources.append(self.source)
            Rule.initialized = True
        if self.source not in Rule.sources:
            print(f"Oh no! {self.source} is not one of {Rule.sources}!")
            raise SourceNotPrecedentedError
        if self.target not in Rule.sources:
            Rule.sources.append(self.target)
        print(Rule.sources)

    def validate(self):
        #self._source_is_precedented()
        self._source_matchfield_is_integer()
        self._target_sortorder_is_integer()
        self._source_matchpattern_is_valid()
        self._source_filename_valid()
        self._target_filename_valid()
        self._source_not_equal_target()
        return self

    def _source_matchfield_is_integer(self):
        try:
            self.source_matchfield = int(self.source_matchfield)
        except:
            print(f"In rule: {self}")
            print(f"source_matchfield is not an integer")
            raise NotIntegerError
        return True

    def _target_sortorder_is_integer(self):
        try:
            self.target_sortorder = int(self.target_sortorder)
        except:
            print(f"In rule: {self}")
            print(f"target_sortorder is not an integer")
            raise NotIntegerError
        return True

    def _source_matchpattern_is_valid(self):
        try:
            re.compile(self.source_matchpattern)
        except re.error:
            raise BadRegexError
        return True

    def _source_filename_valid(self):
        for c in self.source: 
            if c not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.source} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def _target_filename_valid(self):
        for c in self.target: 
            if c not in VALID_FILENAME_CHARS:
                print(f"In rule: {self}")
                print(f"filename {self.target} has invalid character(s).")
                print(f"Valid: {VALID_FILENAME_CHARS}")
                raise NotValidFilenameError
        return True

    def _source_not_equal_target(self):
        if self.source == self.target:
            raise SourceEqualsTargetError
        return True

    def apply_rule_to(self, dataline):

        for line in all[src]:

            # @@@ change field names
            # skip match if in_field out of range
            if in_field > len(line.split()):
                continue

            # match against entire line if in_field exactly zero
            if in_field == 0:
                all[trg].extend([x for x in all[src] if re.search(rgx, x)])
                all[src] = [x for x in all[src] if not re.search(rgx, x)]

            # match given field if in_field greater than zero and within range
            if in_field > 0:
                y = in_field - 1
                all[trg].extend([x for x in all[src]
                                 if re.search(rgx, x.split()[y])])
                all[src] = [x for x in all[src]
                            if not re.search(rgx, x.split()[y])]

            # sort target if sort_awkf greater than zero
            if sort_awkf:
                sort_ethf = sort_awkf - 1
                decorated = [(line.split()[sort_ethf], __, line)
                             for __, line in enumerate(all[trg])]
                decorated.sort()
                all[trg] = [line for ___, __, line in decorated]

        return all
