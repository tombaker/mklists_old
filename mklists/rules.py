import re
import sys
import string
from textwrap import dedent
from dataclasses import dataclass

class BadRuleString(SystemExit):
    pass

VALID_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

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

def get_stringrules(*rules_files):
    stringrules = []
    for rules_file in rules_files:
        try:
            with open(rules_file, 'r') as rulefile:
                stringrules.extend(rulefile.read().splitlines())
        except FileNotFoundError:
            sys.exit(f'Rule file "{rules_file}" does not exist or is not accessible.')

    return stringrules
            
def stringrule_to_listrule(rulestring):
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

def stringrules_to_listrules(stringrules):
    return [stringrule_to_listrule(line) for line in stringrules if stringrule_to_listrule(line)]

def listrule_backto_stringrule(listrule):
    if len(listrule) > 1:
        listrule[1] = "".join(["/", listrule[1], "/"])
    return " ".join([str(item) for item in listrule])

def listrule_to_stringrule(listrule):
    try:
        listrule[1] = "".join("/", listrule[1], "/")
    except:
        return repr(listrule)
    return " ".join([item for item in listrule])

def exit_for_bad_rule_form(listrule_tested, message):
    if len(listrule_tested) > 1:
        listrule_tested[1] = '/' + listrule_tested[1] + '/'
    print(" ".join(listrule_tested))
    sys.exit(message)

def check_listrules(listrules):
    listrules_checked = []
    for listrule_to_check in listrules:

        # listrule_to_check must have 4 or 5 fields
        if 4 <= len(listrule_to_check) <= 5:
            exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        # field 1 is a digit
        if not listrule_to_check[0].isdigit():
            exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        # field 2 is a valid regular expression
        try:
            re.compile(listrule_to_check[1])
        except:
            exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        # field 3 is a valid filename (according to set of valid characters)
        if not all(c in VALID_CHARS for c in listrule_to_check[2]):
            exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        # field 4 is a valid filename (according to set of valid characters)
        if not all(c in VALID_CHARS for c in listrule_to_check[3]):
            exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        # field 5 is a digit
        if len(listrule_to_check) == 5:
            if not listrule_to_check[4].isdigit():
                exit_for_bad_rule_form(listrule_to_check, CORRECT_RULE_FORM)

        listrules_checked.append(listrule)

    return listrules_checked

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

        # listrule_checked[0] = int(listrule_checked[0])
        # listrule_checked[4] = int(listrule_checked[4])
