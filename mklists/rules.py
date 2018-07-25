import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass

SOME_CONSTANT = "Hello, world!"

def print_constant():
    return SOME_CONSTANT

class BadRuleString(SystemExit):
    pass

VALID_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

# Put this into default .mklistsrc
CORRECT_RULE_FORM = """\
The rule above is incorrectly formed.

Rule must have four or (optionally) five fields:

    3 /x/ a.txt b.txt
    3 /x/ a.txt b.txt 2   # with optional sort order

Fields:

    1. Field against which regex is matched (a digit).
    2. Regex, delimited by slashes.
    3. Source file, lines of which are tested for matches.
    4. Target file, destination of matching lines.
    5. Sort order of target file

In pseudo-code:

    for each line in source a.txt
        if regex /x/ matches third field (the "match field")
            move line from a.txt to b.txt
            sort b.txt on second field (if optional sort order given)
        if regex /x/ does not match third field
            do nothing

Note:
-- If match field is 0, entire line (with whitespace) matched.
-- If match field is greater than line length, match is ignored.
-- Regex must escape forward slashes - eg "/\/n/".
-- Regex may include spaces - eg "/^From /"
-- Whitespace is ignored except within regex (between first and last slash).
-- Comments (everything after a pound sign) are ignored.
-- Fields 3 and 4 are (configurably) valid filenames not containing slashes.
"""

def get_srules(*rules_files):
    srules = []
    for rules_file in rules_files:
        try:
            with open(rules_file, 'r') as rulefile:
                srules.extend(rulefile.read().splitlines())
        except FileNotFoundError:
            sys.exit(f'Rule file "{rules_file}" does not exist or is not accessible.')

    return srules
            
def srule_to_lrule(rulestring):
    fields = []
    in_field, __, rest = rulestring.partition('/')
    fields.append(in_field.strip())
    regex, __, rest = rest.rpartition('/')
    fields.append(regex)
    rest = rest.partition('#')[0].strip()
    fields.extend(rest.split())
    fields = [field for field in fields if not re.match('#', field)]
    fields = [field for field in fields if field]
    return fields

def srules_to_lrules(srules):
    return [srule_to_lrule(line) for line in srules if srule_to_lrule(line)]

def lrule_backto_srule(lrule):
    if len(lrule) > 1:
        lrule[1] = "".join(["/", lrule[1], "/"])
    return " ".join([str(item) for item in lrule])

def lrule_to_srule(lrule):
    try:
        lrule[1] = "".join("/", lrule[1], "/")
    except:
        return repr(lrule)
    return " ".join([item for item in lrule])

def exit_for_bad_rule_form(lrule_tested, message):
    if len(lrule_tested) > 1:
        lrule_tested[1] = '/' + lrule_tested[1] + '/'
    print(" ".join(lrule_tested))
    sys.exit(message)

def check_lrules(lrules):
    lrules_checked = []
    for lrule_to_check in lrules:
        # lrule_to_check must have 4 or 5 fields
        if 4 <= len(lrule_to_check) <= 5:
            exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        # field 1 is a digit
        if not lrule_to_check[0].isdigit():
            exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        # field 2 is a valid regular expression
        try:
            re.compile(lrule_to_check[1])
        except:
            exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        # field 3 is a valid filename (according to set of valid characters)
        if not all(c in VALID_CHARS for c in lrule_to_check[2]):
            exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        # field 4 is a valid filename (according to set of valid characters)
        if not all(c in VALID_CHARS for c in lrule_to_check[3]):
            exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        # field 5 is a digit
        if len(lrule_to_check) == 5:
            if not lrule_to_check[4].isdigit():
                exit_for_bad_rule_form(lrule_to_check, CORRECT_RULE_FORM)

        lrules_checked.append(lrule)

    return lrules_checked

# Field 2, a regex
#    def exit_rule_regex_must_be_escaped(line):
#        print("In rule: %r" % line)
#        print("...in order to match the regex string: %r" % linesplitonorbar[1])
#        print("...the rule component must be escaped as follows: %r" % re.escape(linesplitonorbar[1])
# No source 
#    probably because not yet created by target
# $3 = re.compile($3)
# filenames must have only permitted characters
# try:
#     re.compile('he(lo')

@dataclass
class Rule:
    """ 
    srcmatch_awkf 
    srcmatch_rgx 
    src 
    trg 
    trgsort_awkf
    """

# test for content of error message too:
# https://stackoverflow.com/questions/30256332/verify-the-the-error-code-or-message-from-systemexit-in-pytest

# In [6]: try:
# ...:     re.compile(pattern)
# ...: except:
# ...:     print('oops')

        # lrule_checked[0] = int(lrule_checked[0])
        # lrule_checked[4] = int(lrule_checked[4])
