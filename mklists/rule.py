import re
from textwrap import dedent
from dataclasses import dataclass

def get_rulestrings(rulefile):
    """what if rulefile does not exist?"""
    with open(rulefield, 'r') as rulefile:
        return rulefile.read().splitlines()

class RuleFile(object):
    """ print(rulefilename)
        NoRuleFileError('Rule file does not exist or is unusable.')
    """

class BadRuleString(SystemExit):

    def __str__(self):
        return """\
                Correct form: '3 /x/ a.txt b.txt 2' - means:

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

def stringrules_to_listrules(rulestrings):
    return [stringrule_to_listrule(line) for line in rulestrings if stringrule_to_listrule(line)]

def check_rulestrings2rules(rulestrings):
    """asdf"""

def lines2rulestrings2(rulestrings):
    fielded_rules = []
    for rulestring in rulestrings:
        fields = []
        in_field, __, rest = rulestring.partition('/')
        fields.append(in_field.strip())
        regex, __, rest = rest.rpartition('/')
        fields.append(regex)
        rest = rest.partition('#')[0].strip()
        if not rest:
            continue
        fields.extend(rest.split())
        fielded_rules.append(fields)
    for rule in fielded_rules:
        if not rule[0].isdigit():
            print(repr(rulestring))
            raise BadRuleString
        rule[0] = int(rule[0])
    return fielded_rules


@dataclass
class Rule:
    """ 
    srcmatch_awkf 
    srcmatch_rgx 
    src 
    trg 
    trgsort_awkf
    """

