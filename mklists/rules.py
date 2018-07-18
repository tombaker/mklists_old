import re
import sys
from textwrap import dedent
from dataclasses import dataclass

class RuleFile(object):
    """ print(rulefilename)
        NoRuleFileError('Rule file does not exist or is unusable.')
    """

class BadRuleString(SystemExit):

    def __str__(self):
        return """\
                Example: '3 /x/ a.txt b.txt 2'

                for each line in source a.txt
                    if regex /x/ matches third field (the "match field")
                        move line from a.txt to b.txt
                        sort b.txt on second field

                Note:
                -- if match field is 0, entire line (with whitespace) matched
                -- if match field is greater than line length, match is ignored
                -- regex must escape forward slashes - eg "/\/n/"
                -- regex may include spaces - eg "/^From /"
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

def check_listrules(listrules):
    """2018-07-17: does not 'see' the liststring
    Could test for content of error message too:
    https://stackoverflow.com/questions/30256332/verify-the-the-error-code-or-message-from-systemexit-in-pytest
    """
    for listrule in listrules:
        if not listrule[0].isdigit():
            stringrule = " ".join([listrule[0], "/", listrule[1], "/", listrule[2], listrule[3], listrule[4]])
            print(repr(stringrule))
            raise BadRuleString
        listrule[0] = int(listrule[0])
    return listrules

# Entire line must be five fields long
# Fields 1 and 5 must be digits
#    if rule[0].isdigit
#    if rule[4].isdigit
# Field 2, a regex
#    def exit_rule_regex_must_be_escaped(line):
#        print("In rule: %r" % line)
#        print("...in order to match the regex string: %r" % linesplitonorbar[1])
#        print("...the rule component must be escaped as follows: %r" % re.escape(linesplitonorbar[1])
# No source 
#    probably because not yet created by target
# $1.isdigit()  - which includes zero
# $5.isdigit()  - which includes zero
# $1 = int($1)
# $5 = int($1)
# except SourceMatchAndTargetSortOrderDigits:
# $3 = re.compile($3)
# $4 and $5:
# must have only permitted characters
# valid_chars = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)
# if it gets this far:
# append line to rules_l


@dataclass
class Rule:
    """ 
    srcmatch_awkf 
    srcmatch_rgx 
    src 
    trg 
    trgsort_awkf
    """

